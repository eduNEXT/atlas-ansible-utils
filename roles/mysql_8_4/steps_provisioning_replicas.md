# Steps for provisioning Mysql replica

This guide is designed to help you correctly provision and configure a MySQL database replica.

## Steps

### 1. Configuration in manifest

In host.ini, you need to add the replica and primary instances, for example:

```ini
[mysql_master]
<master ip>     MYSQL_CONFIG_SERVER_ID=1 COMMON_HOSTNAME=mysql-master ansible_user=ubuntu

[mysql_replicas]
<replica ip>    MYSQL_CONFIG_SERVER_ID=2 COMMON_HOSTNAME=mysql-replica ansible_user=ubuntu

[mysql_servers:children]
mysql_master
mysql_replicas

```

In group_vars, you need to add the necessary values for the replica instance, for example:

```yaml
MYSQL_VOLUMES:
  - device: /dev/nvme1n1
    mount: /var/lib/mysql
    options: "defaults,nofail"
    fstype: xfs
    size: "300.00 GB"
  - device: /dev/nvme2n1
    mount: /backups
    options: "defaults,nofail"
    fstype: xfs
    size: "60.00 GB"

MYSQL_CONFIG_DATABASES: []
MYSQL_CONFIG_USERS: []

MYSQL_CONFIG_MAX_CONNECTIONS: 600
MYSQL_CONFIG_OPEN_FILES_LIMIT: 3000
MYSQL_CONFIG_INNODB_BUFFER_POOL_SIZE: 3G
MYSQL_CONFIG_INNODB_IO_CAPACITY: 500
MYSQL_CONFIG_INNODB_IO_CAPACITY_MAX: 1000
MYSQL_CONFIG_INNODB_LOG_FILE_SIZE: 512M
MYSQL_CONFIG_INNODB_LOG_BUFFER_SIZE: 128M
MYSQL_CONFIG_INNODB_READ_IO_THREADS: 4
MYSQL_CONFIG_INNODB_WRITE_IO_THREADS: 4
MYSQL_CONFIG_INNODB_FLUSH_LOG_AT_TRX_COMMIT: 1
MYSQL_CONFIG_EXPIRE_LOGS_DAYS: 3
```

### 2. Playbook

Run the mysql_8_4 playbook using the **--limit** flag to specify the replica instance, for example:

`ansible-playbook playbooks/mysql_8_4.yml -i ../<manifest>/ansible_inventory/hosts.ini -v --limit mysql_replicas`

### 3. Master and replica configuration

If the databases it's **not** in producction can follow the next steps in this documentation: [Configuring Replication](https://dev.mysql.com/doc/refman/8.4/en/replication-configuration.html)

However, if the databases are in production, step “19.1.2.4 Obtaining the Replication Source Binary Log Coordinates” can cause problems because when we execute `FLUSH TABLES WITH READ LOCK;` we stop writing to the tables. In the case of production, it is advisable to skip that command and continue with the following steps.

### 4. Common problems

In many cases, event replication problems may arise. When checking the replication status, you may encounter the following:

```bash
mysql> SHOW REPLICA STATUS\G
*************************** 1. row ***************************
Replica_IO_State: Waiting for source to send event
Source_Host: x.x.x.x
Source_User: replicator
Source_Port: 3306
Connect_Retry: 60 
Source_Log_File: mysql-bin.000001 
Read_Source_Log_Pos: 530289431 
Relay_Log_File: mysql-replica-relay-bin.000002 
Relay_Log_Pos: 320 
Relay_Source_Log_File: mysql-bin.000001 
Replica_IO_Running: Yes 
Replica_SQL_Running: No 
.
.
.
Replicate_Wild_Ignore_Table: 
    Last_Errno: 1062 
    Last_Error: Coordinator stopped because there were error(s) in the worker(s). The most recent failure being: Worker 4 failed executing transaction 'ANONYMOUS' at source log mysql-bin.000001, end_log_pos 447225645. See error log and/or performance_schema.replication_applier_status_by_worker table for more details about this failure or others, if any. 
    Skip_Counter: 0
.
.
.
```

In these cases, it is necessary to review the error in detail by running ```SELECT *
FROM performance_schema.replication_applier_status_by_worker
WHERE CHANNEL_NAME = ‘’;```

If the transaction you are trying to apply is already the same in both instances (master and replica), you can follow these steps to skip this error **(Be careful and check carefully if this transaction is necessary)**:
```sql
STOP REPLICA;
SET GLOBAL SQL_SLAVE_SKIP_COUNTER = 1;
START REPLICA;
```

After this, when checking the status of the replica, you should see the following:
```sql
Replica_IO_Running: Yes 
Replica_SQL_Running: Yes 
```

