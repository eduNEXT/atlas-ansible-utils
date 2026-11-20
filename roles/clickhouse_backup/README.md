# CLICKHOUSE BACKUP ROLE

Backs up ClickHouse with its native `BACKUP` command, straight to object
storage (AWS S3 or S3-compatible, Azure Blob Storage).

Only ClickHouse is used: nothing is dumped to the local disk and no extra tool
is installed. The role decides what to back up, runs `BACKUP`, and waits for
the result. **It never deletes backups**: retention is done by lifecycle rules
on the bucket (see [Retention](#retention-lifecycle-rules)).

Run it with `playbooks/clickhouse_backup.yml`, usually from a CronJob of the
`ansible-runner` chart (see [Scheduling](#scheduling)).

## Backup kinds

Set `CLICKHOUSE_BACKUP_KIND`:

| Kind | What it does | Meant for |
|------|--------------|-----------|
| `incremental` | A base (full) backup per cycle, then incrementals against that base | Frequent restore points using little storage |
| `full` | A standalone full backup on every run, no incrementals | Keeping full copies that do not depend on any other backup |

Both kinds are independent and can run side by side (two CronJobs).

### `incremental`: base + incrementals

```
<root>/incremental/<cycle>/base-<YYYYMMDDTHHMMSSZ>
<root>/incremental/<cycle>/incr-<YYYYMMDDTHHMMSSZ>
```

- `CLICKHOUSE_BACKUP_CYCLE` is `weekly` (ISO week, e.g. `2026-W46`) or
  `monthly` (e.g. `2026-11`).
- The first run of a new cycle creates the base. Every other run of that cycle
  creates an incremental against the base.
- Every incremental is taken against the **base**, not against the previous
  incremental. Restoring one only needs the base and that incremental.
- A base is complete when its `.backup` file exists (ClickHouse writes it
  last). The role finds it with a `SELECT` on the `s3()` (or
  `azureBlobStorage()`) table function. If a base fails, its files are ignored,
  the next run creates a new base, and the lifecycle rule removes the leftovers.

To restore, point `RESTORE` at the incremental only; ClickHouse reads the base
automatically:

```sql
RESTORE DATABASE db FROM S3('https://<bucket>.s3.<region>.amazonaws.com/<root>/incremental/<cycle>/incr-<id>');
```

### `full`: standalone full backups

```
<root>/full/<YYYYMMDDTHHMMSSZ>
```

## Retention (lifecycle rules)

Retention is configured on the bucket, one rule per prefix:

| Prefix | Expire after | Why |
|--------|--------------|-----|
| `<root>/incremental/` | cycle length × 2 + 1 day: **15 days** (`weekly`), **63 days** (`monthly`) | Keeps the previous cycle complete until the current one has its base |
| `<root>/full/` | full backup interval × copies to keep + 1 day (e.g. **8 days** for one weekly copy) | Full backups are standalone, any age is safe |

Why this is safe for incrementals: a base is the oldest object of its cycle,
and every incremental of that cycle depends only on it. With the expiration
above, a base is only removed when the next cycle is complete and the current
cycle already has its base. The incrementals of the expired cycle are then
unusable for a few days, until they expire too; newer backups exist.

The cycle and the expiration must match: if you change
`CLICKHOUSE_BACKUP_CYCLE`, change the rule too. Lifecycle rules never delete
earlier than configured, but they may delete later.

**Lifecycle rules delete even when backups are failing.** If the CronJob stops
working for longer than the expiration, there are no backups left. Alert on
failed backup Jobs.

Terraform example (AWS):

```hcl
resource "aws_s3_bucket_lifecycle_configuration" "clickhouse_backups" {
  bucket = aws_s3_bucket.clickhouse_backups.id

  rule {
    id     = "clickhouse-incremental"
    status = "Enabled"
    filter {
      prefix = "clickhouse/incremental/"
    }
    expiration {
      days = 15
    }
    abort_incomplete_multipart_upload {
      days_after_initiation = 1
    }
  }

  rule {
    id     = "clickhouse-full"
    status = "Enabled"
    filter {
      prefix = "clickhouse/full/"
    }
    expiration {
      days = 8
    }
    abort_incomplete_multipart_upload {
      days_after_initiation = 1
    }
  }
}
```

With bucket versioning enabled, also add `noncurrent_version_expiration`;
otherwise expired objects are kept as noncurrent versions.

Azure (untested): use a lifecycle management policy with the same prefixes
(`prefixMatch: <container>/<root>/incremental/`) and
`daysAfterModificationGreaterThan`.

## Storage and credentials

Set `CLICKHOUSE_BACKUP_STORAGE_OPTIONS` (see `defaults/main.yml`).

| Storage | Credentials | Status |
|---------|-------------|--------|
| AWS S3 | `instance`: IAM role attached to the instance, no keys | Tested (ClickHouse 25.3) |
| AWS S3 | `static`: access key of an IAM user | Untested |
| S3-compatible | `static` + `S3_ENDPOINT_URL` | Untested |
| Azure Blob Storage | account key | **Untested, needs validation** |

Temporary AWS credentials (with a session token, e.g. from an assumed role)
do **not** work: in ClickHouse 25.3, `BACKUP ... TO S3()` only accepts
`url` or `url, access_key_id, secret_access_key`.

The IAM role (or user) needs, on the bucket: `s3:ListBucket`,
`s3:GetBucketLocation`, and on its objects: `s3:PutObject`, `s3:GetObject`,
`s3:AbortMultipartUpload`, `s3:ListMultipartUploadParts`.

It does **not** need `s3:DeleteObject`: without it, someone with access to the
ClickHouse host cannot delete the backups.

## What is backed up

- `CLICKHOUSE_BACKUP_SCOPE: all` (default): every database except
  `CLICKHOUSE_BACKUP_EXCLUDED_DATABASES`.
- `CLICKHOUSE_BACKUP_SCOPE: databases`: only `CLICKHOUSE_BACKUP_DATABASES`.

Extra `BACKUP` settings (e.g. `s3_storage_class`, `max_backup_bandwidth`) go in
`CLICKHOUSE_BACKUP_EXTRA_SETTINGS`.

## How a run works

1. Validate the configuration.
2. Plan: `base`, `incremental` or `full`, and the target path. For `incremental`,
   look for a complete base of the current cycle.
3. `BACKUP ... ASYNC`, then poll `system.backups` until the backup finishes
   (`CLICKHOUSE_BACKUP_TIMEOUT_SECONDS`).
4. Fail with the ClickHouse error if the status is not `BACKUP_CREATED`.

The ClickHouse password is written to a `clickhouse-client` config file
(`0600`, in `CLICKHOUSE_BACKUP_CONFIG_DIR`) so it never shows up in the
process list.

## Scheduling

Use the `ansible-runner` chart, one CronJob per kind:

```yaml
jobs:
  - name: clickhouse-backup-incremental
    playbook: clickhouse_backup
    schedule: "0 3 * * *"
    suspend: false
    concurrencyPolicy: Forbid
    extraEnvs:
      - name: ATLAS_ANSIBLE_PLAYBOOK_EXTRA_PARAMS
        value: -e CLICKHOUSE_BACKUP_KIND=incremental
  - name: clickhouse-backup-full
    playbook: clickhouse_backup
    schedule: "0 5 * * 0"
    suspend: false
    concurrencyPolicy: Forbid
    extraEnvs:
      - name: ATLAS_ANSIBLE_PLAYBOOK_EXTRA_PARAMS
        value: -e CLICKHOUSE_BACKUP_KIND=full
```

Use `concurrencyPolicy: Forbid`: two `incremental` runs at the start of a cycle
would create two bases.
