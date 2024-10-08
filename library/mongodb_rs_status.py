from __future__ import absolute_import
from six.moves import map
DOCUMENTATION = """
---
module: mongodb_rs_status
short_description: Get the status of a replica set of a mongo cluster.
description:
  - Get the status of the replica set of a mongo cluster. Provide the same info as rs.status() or replSetGetStatus.
    Returns a status dictionary key containing the replica set JSON document from Mongo, or no status key if there
    was no status found.  This usually indicates that either Mongo was configured to run without replica sets or
    that the replica set has not been initiated yet.
version_added: "1.9"
author:
  - Feanil Patel
  - Kevin Falcone
options:
  host:
    description:
      - The hostname or ip of a server in the mongo cluster.
    required: false
    default: 'localhost'
  port:
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
    required: false
"""

EXAMPLES = '''
- name: Get status for the stage cluster
  mongodb_rs_status:
    host: localhost:27017
    username: root
    password: password
  register: mongo_status
Note that you're testing for the presence of the status member of the dictionary not the contents of it
- debug: msg="I don't have a replica set available"
  when: mongo_status.status is not defined
- debug: var=mongo_status.status
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

import json
from six.moves.urllib.parse import quote_plus

def main():

    arg_spec = dict(
        host=dict(required=False, type='str', default="localhost"),
        port=dict(required=False, type='int', default=27017),
        username=dict(required=False, type='str'),
        password=dict(required=False, type='str'),
        auth_database=dict(required=False, type='str')
    )

    module = AnsibleModule(argument_spec=arg_spec, supports_check_mode=False)

    if not pymongo_found:
        module.fail_json(msg="The python pymongo module is not installed.")

    mongo_uri = 'mongodb://'
    host = module.params.get('host')
    port = module.params.get('port')
    username = module.params.get('username')
    password = module.params.get('password')
    auth_database = module.params.get('auth_database')

    if (username and not password) or (password and not username):
        module.fail_json(msg="Must provide both username and password or neither.")

    if username:
        mongo_uri += "{}:{}@".format(*list(map(quote_plus, [username,password])))

    mongo_uri += "{}:{}".format(quote_plus(host),port)

    if auth_database:
        mongo_uri += '/{}'.format(quote_plus(auth_database))

    # The directConnection parameter was changed in Pymongo 4.x.x. More details in
    # https://pymongo.readthedocs.io/en/stable/migrate-to-pymongo4.html#directconnection-defaults-to-false
    client = MongoClient(mongo_uri, directConnection=True)

    # This checks to see if you have a replSetName configured
    # This generally means that /etc/mongod.conf has been changed
    # from the default to use a replica set and mongo has been
    # restarted to use it.

    try:
        repl_set = client.admin.command('getCmdLineOpts')['parsed']['replication']['replSetName']
    except (OperationFailure, KeyError):
        module.exit_json(changed=False)

    # If mongo was started with a repl_set, it is safe to run replSetGetStatus
    if repl_set:
        status = client.admin.command("replSetGetStatus")
    else:
        module.exit_json(changed=False)

    # This converts the bson into a python dictionary that ansible's standard
    # jsonify function can process and output without throwing errors on bson
    # types that don't exist in JSON
    clean = json.loads(json_util.dumps(status))

    module.exit_json(changed=False, status=clean)

if __name__ == '__main__':
    main()
