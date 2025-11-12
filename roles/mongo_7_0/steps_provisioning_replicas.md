Steps for provisioning mongo replicas
=====================================

This is a guide for provisioning and configuring mongod on replica instance.

Normally, for Mongo replicas, you need two replicas and one primary instance. Or, failing that, a primary, a replica, or an arbitrator. In this case, only the first case is explained.

**Note:** In this case, it is assumed that the primary instance is already running MongoDB and has been previously configured.

steps
------

### 1. Configuration in the manifest

In hosts.ini, specify which is the primary host and which will be the secondary hosts, for example:

```ini
[mongo_primary]
<ip host primary>     COMMON_HOSTNAME=mongo_instance ansible_user=ubuntu

[mongo_replica_1]
<ip host replica 1>     COMMON_HOSTNAME=mongo-replica1-instance ansible_user=ubuntu

[mongo_replica_2]
<ip host replica 2>     COMMON_HOSTNAME=mongo-replica2-instance ansible_user=ubuntu

[mongo_servers:children]
mongo_primary
mongo_replica_1
mongo_replica_2

```
Since the primary instance already has a replica_set configured, the playbook may throw an error when attempting to configure a replica set for each replica, causing an error since MongoDB does not allow partial replica sets for replicas.

Therefore, you must set the ```mongo_configuration_replica_set``` variable to **false** in the group_vars configuration of the replicas.
This will skip the steps for configuring the replicasets on the replicas.

### 2. Playbook

Run the mongo_7_0 Playbook using the --limit flag to specify the instance to provision, for example

```ansible-playbook playbooks/mongo_7_0.yml -i ../<manifest>/ansible_inventory/hosts.ini -v --limit mongo_replica_1```

### 3. Configuration on the primary instance

Once MongoDB is operational on both replicas, you only need to enter the mongosh on the primary instance and add the replicas manually with ```rs.add("<ip replica>:27017")```.

You must wait a few minutes for the replica to become operational. You can validate it by running ```rs.status()``` and checking that both the primary and the configured replicas are present, as in the following example:
``` bash
    .
    .
    .
  members: [
    {
      _id: 0,
      name: 'ip-x.x.x.x:27017',
      health: 1,
      state: 1,
      stateStr: 'PRIMARY',
      .
      .
      .
    },
    {
      _id: 1,
      name: 'x.x.x.x:27017',
      health: 1,
      state: 2,
      stateStr: 'SECONDARY',
      .
      .
      .
    },
    {
      _id: 2,
      name: 'x.x.x.x:27017',
      health: 1,
      state: 2,
      stateStr: 'SECONDARY',
      uptime: 74657,
      .
      .
      .
    }
  ],
  .
  .
  .
```