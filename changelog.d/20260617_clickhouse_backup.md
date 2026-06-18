### Added

- A new `clickhouse_backup` role and playbook that creates ClickHouse native
  database backups on local disk and uploads them to S3 or Azure using the
  existing `storage_backups` role. The role integrates with the Docker-based
  `clickhouse_docker` deployment layout and also supports native package
  installations.
