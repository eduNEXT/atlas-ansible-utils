# MongoDB Replica Set Patch Upgrade ( for instance 7.0.x → 7.0.y) using `eduNEXT/atlas-ansible-utils`

This guide describes a **rolling (in-place) patch upgrade** of a **3-member MongoDB replica set** (example: **7.0.7 → 7.0.28**) where MongoDB instances are deployed and updated using the `atlas-ansible-utils` Ansible playbooks.

> **Scope**
>
> - Applies to **patch upgrades inside the same major/minor**, e.g. `7.0.7` → `7.0.28`.
> - Assumes a standard replica set topology: **1 primary + 2 secondaries**.
> - Goal: keep the replica set available by upgrading **one member at a time**, upgrading **secondaries first**, then **stepping down the primary** and upgrading it last.

---

## Preconditions / Safety Checks

1. **Schedule a maintenance window**
  - A primary step-down triggers an election; **writes may pause briefly** during failover (usually seconds). Ensure application retry logic is in place.

2. **Backups**
  - Verify you have a recent backup/snapshot and a validated restore path.

3. **Replica set health**
  - From `mongosh` (connect to the current primary):
    ```javascript
    rs.status()
    rs.printSecondaryReplicationInfo()
    ```

  - Confirm:
    - All members are `PRIMARY`/`SECONDARY` (no `RECOVERING`, `ROLLBACK`, etc.).
    - At least one secondary is **healthy and caught up** (minimal replication lag).
    - No member is intentionally non-electable (e.g., `priority: 0`) unless you understand the election implications.

4. **Confirm current primary**
   ```javascript
   db.hello()
   // or: rs.status()

## Procedure

1. Update the desired MongoDB patch version in your Ansible inventory

  In your inventory (typically group_vars/all.yaml or equivalent), set:

  ```yaml
  MONGO_VERSION_MAJOR_MINOR: "7.0"
  MONGO_VERSION_PATCH: "28"
  ```

  These variables define the target MongoDB version to be installed. In this example, MongoDB 7.0.28 will be installed.

2. **Upgrade the secondaries (one at a time)**: Upgrade each secondary individually using --limit so only one host is modified per run.

  - Run the playbook for a secondary

    ```bash
    ansible-playbook playbooks/mongo_7_0.yml \
      -i path/to/your/hosts.ini \
      --limit mongo_replica_1 \
      -v
    ```

    Repeat for the second secondary:

    ```bash
    ansible-playbook playbooks/mongo_7_0.yml \
      -i path/to/your/hosts.ini \
      --limit mongo_replica_2 \
      -v
    ```

  - Validate after each secondary upgrade

    After each run, validate the upgraded node and replica set health. On the upgraded host:

    ```bash
    mongod --version
    ```

    From mongosh (primary is fine):

    ```javascript
    rs.status()
    rs.printSecondaryReplicationInfo()
    ```

    Wait until the upgraded member is back to SECONDARY and caught up before moving to the next node.

3. Step down the primary (promote a secondary) and upgrade the former primary. At this point both secondaries are on the new patch version; now you will:

  - Step down the current primary to force an election,
  - Upgrade the former primary (now a secondary),
  - Validate the replica set returns to a healthy state.

**Step down the current primary (recommended approach)**

From mongosh connected to the current primary:

```javascript
rs.stepDown(600, 60)
// Step down for 10 minutes (600s), waiting up to 60s for a caught-up secondary.
```

Then confirm a new primary was elected:

```javascript
rs.status()
```

> **_NOTE:_** The step-down window prevents the old primary from immediately being re-elected while you upgrade it.

**Upgrade the former primary using Ansible**

Once the old primary is in SECONDARY state, upgrade it with the playbook.

**Important**: Ensure the playbook run does not attempt to (re)initialize the replica set configuration if that is controlled by your inventory. If your inventory supports it, disable replica set configuration during this step. Example (one of the following approaches):

Approach A — Set in inventory temporarily (host_vars/group_vars)

```yaml
mongo_configure_replica_set: false
```

Approach B — Pass as extra-vars for this run only

```bash
ansible-playbook playbooks/mongo_7_0.yml \
  -i path/to/your/hosts.ini \
  --limit mongo_primary \
  -e "mongo_configure_replica_set=false" \
  -v
```

**Validate the replica set returns to a healthy state**

After the playbook completes, run on the upgraded former primary host:

```bash
mongod --version
```

From mongosh:

```javascript
rs.status()
rs.printSecondaryReplicationInfo()
```

Ensure the upgraded node re-joins as SECONDARY and replication is healthy.

**Cleanup**: If you set mongo_configure_replica_set: false temporarily, remove it after the maintenance to restore your default provisioning behavior.

4. Post-upgrade validation (cluster-wide)

From mongosh (connect to the primary):

```javascript
rs.status()
db.adminCommand({ buildInfo: 1 })
```

Confirm:

- All members are PRIMARY/SECONDARY and healthy.
- All mongod processes report the expected patch version (7.0.28 in this example).
- Replication lag is within acceptable bounds.
