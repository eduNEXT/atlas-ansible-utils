from __future__ import absolute_import
from six.moves import filter
from six.moves import map
from six.moves import range
from six.moves import zip
DOCUMENTATION = """
---
module: mongodb_replica_set
short_description: Modify replica set config.
description:
  - Modify replica set config, including modifying/adding/removing members from a replica set
    changing replica set options, and initiating the replica set if necessary.
    Uses replSetReconfig and replSetInitiate.
version_added: "1.9"
author:
  - Max Rothman
  - Feanil Patel
options:
  rs_host:
    description:
      - The hostname or ip of a server already in the mongo cluster.
    required: false
    default: 'localhost'
  rs_port:
    description:
      - The port to connect to mongo on.
    required: false
    default: 27017
  username:
    description:
      - The username of the mongo user to connect as.
    required: false
  password:
    description:
      - The password to use when authenticating.
    required: false
  auth_database:
    description:
      - The database to authenticate against.
    requred: false
  force:
    description: Whether to pass the "force" option to replSetReconfig.
      For more details, see `<https://docs.mongodb.org/manual/reference/command/replSetReconfig/>`
    required: false
    default: false
  rs_config:
    description: A `replica set configuration document <https://docs.mongodb.org/manual/reference/replica-configuration/>`.
        This structure can be a valid document, but this module can also manage some details for you:
        - members can have separate ``host`` and ``port`` properties. ``port`` defaults to 27017.
          To override this, provide a ``host`` like ``somehost:27017``.
        - ``_id`` is automatically managed if not provided
        - members' ``_id`` are automatically managed
        - ``version`` is automatically incremented
    required: true
"""

EXAMPLES = '''
- name: Basic example
  mongodb_replica_set:
    username: root
    password: password
    rs_config:
      members:
        - host: some.host
        - host: other.host
          port: 27018
          hidden: true
- name: Fully specify a whole document
  mongodb_replica_set:
    username: admin
    password: password
    rs_config:
      _id: myReplicaSetName
      version: 5
      members:
        - _id: 1
          host: some.host:27017
        - _id: 2
          host: other.host:27017
          hidden: true
'''
# Magic import
from ansible.module_utils.basic import *

try:
    from pymongo import MongoClient
    from pymongo.errors import OperationFailure
    from bson import json_util
except ImportError:
    pymongo_found = False
else:
    pymongo_found = True

import json, copy
from six.moves.urllib.parse import quote_plus
from operator import itemgetter

########### Mongo API calls ###########
def get_replset():
    # Not using `replSetGetConfig` because it's not supported in MongoDB 2.x.
    try:
        rs_config = client.local.system.replset.find_one()
    except OperationFailure as e:
        return None

    return rs_config

def initialize_replset(rs_config):
    try:
        client.admin.command("replSetInitiate", rs_config)
    except OperationFailure as e:
        module.fail_json(msg="Failed to initiate replSet: {}".format(e.message))

def reconfig_replset(rs_config):
    try:
        client.admin.command("replSetReconfig", rs_config, force=module.params['force'])
    except OperationFailure as e:
        module.fail_json(msg="Failed to reconfigure replSet: {}".format(e.message))

def get_rs_config_id():
    try:
        return client.admin.command('getCmdLineOpts')['parsed']['replication']['replSetName']
    except (OperationFailure, KeyError) as e:
        module.fail_json(msg=("Unable to get replSet name. "
            "Was mongod started with --replSet, "
            "or was replication.replSetName set in the config file? Error: ") + e.message)


########### Helper functions ###########
def set_member_ids(members, old_members=None):
    '''
    Set the _id property of members who don't already have one.
    Prefer the _id of the "matching" member from `old_members`.
    '''
    #Add a little padding to ensure we don't run out of IDs
    available_ids = set(range(len(members)*2))
    available_ids -= {m['_id'] for m in members if '_id' in m}
    if old_members is not None:
        available_ids -= {m['_id'] for m in old_members}
    available_ids = list(sorted(available_ids, reverse=True))

    for member in members:
        if '_id' not in member:
            if old_members is not None:
                match = get_matching_member(member, old_members)
                member['_id'] = match['_id'] if match is not None else available_ids.pop()
            else:
                member['_id'] = available_ids.pop()

def get_matching_member(member, members):
    '''Return the rs_member from `members` that "matches" `member` (currently on host)'''
    match = [m for m in members if m['host'] == member['host']]
    return match[0] if len(match) > 0 else None

def members_match(new, old):
    "Compare 2 lists of members, discounting their `_id`s and matching on hostname"
    if len(new) != len(old):
        return False
    for old_member in old:
        new_member = get_matching_member(old_member, new).copy()
        #Don't compare on _id
        new_member.pop('_id', None)
        old_member = old_member.copy()
        old_member.pop('_id', None)
        if old_member != new_member:
            return False
    return True

def fix_host_port(rs_config):
    '''Fix host, port to host:port'''
    if 'members' in rs_config:
        if not isinstance(rs_config['members'], list):
            module.fail_json(msg='rs_config.members must be a list')

        for member in rs_config['members']:
            if ':' not in member['host']:
                member['host'] = '{}:{}'.format(member['host'], member.get('port', 27017))
                if 'port' in member:
                    del member['port']

def check_config_subset(old_config, new_config):
    '''
    Compares the old config (what we pass in to Mongo) to the new config (returned from Mongo)
    It is assumed that old_config will be a subset of new_config because Mongo tracks many more
    details about the replica set and the members in a replica set that we don't track in our
    secure repo.
    '''

    for k in old_config:
        if k == 'members':
            matches = is_member_subset(old_config['members'],new_config['members'])
            if not matches: return False
        else:
            if old_config[k] != new_config[k]: return False

    return True


def is_member_subset(old_members,new_members):
    '''
    Compares the member list of a replica set configuration as specified (old_members)
    to what Mongo has returned (new_members).  If it finds anything in old_members that
    does not match new_members, it will return False.  new_members is allowed to contain
    extra information that is not reflected in old_members because we do not necesarily
    track all of mongo's internal data in the config.
    '''

    # Mongo returns the member set in no particular order, and we were
    # indexing into the list using _id before without sorting which led to failure.
    old_members, new_members = [sorted(k, key=itemgetter('_id'))
        for k in (old_members, new_members)]

    for k1, k2 in zip(old_members, new_members):
        for key, value in k1.items():
            if value != k2[key]: return False

    return True

def update_replset(rs_config):
    changed = False
    old_rs_config = get_replset()
    fix_host_port(rs_config)  #fix host, port to host:port

    #Decide whether we need to initialize
    if old_rs_config is None:
        changed = True
        if '_id' not in rs_config:
            rs_config['_id'] = get_rs_config_id()  #Errors if no replSet specified to mongod
        set_member_ids(rs_config['members'])  #Noop if all _ids are set
        #Don't set the version, it'll auto-set
        initialize_replset(rs_config)

    else:
        old_rs_config_scalars = {k:v for k,v in old_rs_config.items() if not isinstance(v, (list, dict))}

        rs_config_scalars = {k:v for k,v in rs_config.items() if not isinstance(v, (list, dict))}
        if '_id' not in rs_config_scalars and '_id' in old_rs_config_scalars:
            # _id is going to be managed, don't compare on it
            del old_rs_config_scalars['_id']
        if 'version' not in rs_config and 'version' in old_rs_config_scalars:
            # version is going to be managed, don't compare on it
            del old_rs_config_scalars['version']

        # Special comparison to test whether 2 rs_configs are "equivalent"
        # We can't simply use == because of special logic in `members_match()`
        # 1. Compare the scalars (i.e. non-collections)
        # 2. Compare the "settings" dict
        # 3. Compare the members dicts using `members_match()`
        # Since the only nested structures in the rs_config spec are "members" and "settings",
        # if all of the above 3 match, the structures are equivalent.
        if rs_config_scalars != old_rs_config_scalars \
            or rs_config.get('settings') != old_rs_config.get('settings') \
            or not members_match(rs_config['members'], old_rs_config['members']):

            changed=True
            if '_id' not in rs_config:
                rs_config['_id'] = old_rs_config['_id']
            if 'version' not in rs_config:
                #Using manual increment to prevent race condition
                rs_config['version'] = old_rs_config['version'] + 1

            set_member_ids(rs_config['members'], old_rs_config['members'])  #Noop if all _ids are set

            reconfig_replset(rs_config)

    #Validate it worked
    if changed:
        changed_rs_config = get_replset()
        if not check_config_subset(rs_config, changed_rs_config):
            module.fail_json(msg="Failed to validate that the replica set was changed", new_config=changed_rs_config, config=rs_config)

    # Remove settings from changed_rs_config before exit to avoid
    # problem with exit_json() and unserializable ObjectId
    # because MongoDB returns JSON which is not serializable
    if changed_rs_config.get('settings') is not None:
        changed_rs_config['settings'] = None

    module.exit_json(changed=changed, config=rs_config, new_config=changed_rs_config)


######### Client making stuff #########
def get_mongo_uri(host, port, username, password, auth_database):
    mongo_uri = 'mongodb://'
    if username and password:
        mongo_uri += "{}:{}@".format(*list(map(quote_plus, [username,password])))

    mongo_uri += "{}:{}".format(quote_plus(host), port)

    if auth_database:
        mongo_uri += "/{}".format(quote_plus(auth_database))

    return mongo_uri

def primary_client(some_host, some_port, username, password, auth_database):
    '''
    Given a member of a replica set, find out who the primary is
    and provide a client that is connected to the primary for running
    commands.
    Because this function attempts to find the primary of your replica set,
    it can fail and throw PyMongo exceptions.  You should handle these and
    fall back to get_client.
    '''
    client = get_client(some_host, some_port, username, password, auth_database)
    # This can fail (throws OperationFailure), in which case code will need to
    # fall back to using get_client since there either is no primary, or we can't
    # know it for some reason.
    status = client.admin.command("replSetGetStatus")

    # Find out who the primary is.
    rs_primary = [member for member in status['members'] if member['stateStr']=='PRIMARY'][0]
    primary_host, primary_port = rs_primary['name'].split(':')

    # Connect to the primary if this is not the primary.
    if primary_host != some_host or primary_port != some_port:
        client.close()
        new_uri = get_mongo_uri(primary_host, primary_port, username, password, auth_database)
        client = MongoClient(new_uri)

    return client

def get_client(some_host, some_port, username, password, auth_database):
    '''
    Connects to the given host.  Does not have any of the logic of primary_client,
    so is safer to use when handling an uninitialized replica set or some other
    mongo instance that requires special logic.
    This function connects to Mongo, and as such can throw any of the PyMongo
    exceptions.
    '''
    mongo_uri = get_mongo_uri(some_host, some_port, username, password, auth_database)
    # The directConnection parameter was changed in Pymongo 4.x.x. More details in
    # https://pymongo.readthedocs.io/en/stable/migrate-to-pymongo4.html#directconnection-defaults-to-false
    client = MongoClient(mongo_uri, directConnection=True)
    return client

################ Main ################
def validate_args():
    arg_spec = dict(
        username = dict(required=False, type='str'),
        password = dict(required=False, type='str'),
        auth_database = dict(required=False, type='str'),
        rs_host = dict(required=False, type='str', default="localhost"),
        rs_port = dict(required=False, type='int', default=27017),
        rs_config = dict(required=True, type='dict'),
        force = dict(required=False, type='bool', default=False),
    )

    module = AnsibleModule(argument_spec=arg_spec, supports_check_mode=False)

    username = module.params.get('username')
    password = module.params.get('password')
    if (username and not password) or (password and not username):
        module.fail_json(msg="Must provide both username and password or neither.")

    # Check that if votes is 0 priority is also 0
    for member in module.params.get('rs_config').get('members'):
        if member.get('votes') == 0 and member.get('priority') != 0:
            module.fail_json(msg="Non-voting member {} must have priority 0".
                             format(member['host']))

    return module


if __name__ == '__main__':
    module = validate_args()

    if not pymongo_found:
        module.fail_json(msg="The python pymongo module is not installed.")

    username = module.params.get('username')
    password = module.params.get('password')
    auth_database = module.params.get('auth_database')
    rs_host = module.params['rs_host']
    rs_port = module.params['rs_port']

    try:
        client = primary_client(rs_host, rs_port, username, password, auth_database)
    except OperationFailure:
        client = get_client(rs_host, rs_port, username, password, auth_database)

    update_replset(module.params['rs_config'])
