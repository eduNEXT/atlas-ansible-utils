# ClickHouse Backup Role

This role creates database backups with ClickHouse's native `BACKUP` command.
`CLICKHOUSE_BACKUP_STORAGE_TYPE` selects `local` or `s3`; the default is `local`.

The role defaults to backing up all databases to `/mnt/backups` in one archive.
Set `CLICKHOUSE_BACKUP_DATABASES` to a non-empty list to back up only the
specified databases; each selected database is written to its own backup.
`CLICKHOUSE_BACKUP_PATH` can be set to another absolute path. The ClickHouse
server must have permission to write to that path.

For example, to back up only `analytics` and `events`, set:

```yaml
CLICKHOUSE_BACKUP_DATABASES:
  - analytics
  - events
```

The backup account defaults to `CLICKHOUSE_DEFAULT_USER_NAME` and
`CLICKHOUSE_DEFAULT_USER_PASSWORD`. Queries run through
`community.clickhouse.clickhouse_client`; the role installs the
`python3-clickhouse-driver` package required by that module. Backup task output
is suppressed to prevent credential disclosure.

## S3 backups

Set `CLICKHOUSE_BACKUP_STORAGE_TYPE` to `s3`, then configure the bucket, region,
and object prefix:

```yaml
CLICKHOUSE_BACKUP_STORAGE_TYPE: s3
CLICKHOUSE_BACKUP_S3_BUCKET_NAME: example-clickhouse-backups
CLICKHOUSE_BACKUP_S3_REGION: us-east-1
CLICKHOUSE_BACKUP_S3_PREFIX: production/clickhouse
```

`CLICKHOUSE_BACKUP_S3_ENDPOINT` can override the generated AWS endpoint. The
override must be the HTTPS URL for the bucket root, including its trailing
slash. With no override, the role uses the regional path-style AWS endpoint.

Authentication supports either both `CLICKHOUSE_BACKUP_S3_ACCESS_KEY_ID` and
`CLICKHOUSE_BACKUP_S3_SECRET_ACCESS_KEY`, or neither. When both are omitted,
ClickHouse uses environment or EC2 metadata credentials, including the EC2
instance profile. A partial pair fails validation. Static credentials should
be supplied through Ansible Vault; the rendered ClickHouse configuration is
restricted to root and the `clickhouse` group.

The role configures an S3 named collection and submits `BACKUP ... TO S3(...)`
directly to ClickHouse. It does not use AWS CLI to transfer backup files. Each
backup has a host-specific, timestamped path with a per-run identifier below
the selected prefix. The S3 identity needs permission to write backup objects;
ClickHouse's S3 backup documentation also recommends `s3:DeleteObject` for
backups exported to an external bucket. Scope permissions to the bucket and
prefix. S3 lifecycle rules can be used to expire backups.

Example invocation with the S3 settings defined in inventory:

```bash
uv run ansible-playbook playbooks/clickhouse_backup.yml -i hosts-ch.yaml
```
