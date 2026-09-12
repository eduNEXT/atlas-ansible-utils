# ClickHouse Ansible Role

Provisions and configures ClickHouse standalone instances on Ubuntu/Debian.

## Features

- Installs ClickHouse from official repository
- Configures HTTP/native ports, listen hosts
- Manages users, roles, grants via `CLICKHOUSE_USERS`
- Optional custom admin user (replaces `default`)
- Backup disk configuration for `clickhouse-backup`
- System log tables with TTL retention
- Custom configuration snippets via `CLICKHOUSE_CUSTOM_CONFIGS`
- Safe version upgrades (patch/minor auto, major blocked by default)
- EBS volume mounting via `mount_ebs` role (conditional)
- Integration with `clickhouse_backup` role for backup policies

## Requirements

- Ansible 2.12+
- Ubuntu 20.04/22.04/24.04 or Debian 11/12
- `community.general` collection (for `filesystem` module in `mount_ebs`)

## Role Variables

### Version & Upgrade

| Variable | Default | Description |
|----------|---------|-------------|
| `CLICKHOUSE_VERSION` | `"25.8"` | Major.Minor version (patch auto-selected) |
| `CLICKHOUSE_ALLOW_MAJOR_UPGRADE` | `false` | Allow major version upgrades (requires manual backup first) |

### Network

| Variable | Default | Description |
|----------|---------|-------------|
| `CLICKHOUSE_LISTEN_HOSTS` | `["::", "0.0.0.0"]` | Listen addresses |
| `CLICKHOUSE_HOST_INSECURE_HTTP_PORT` | `8123` | HTTP API port |
| `CLICKHOUSE_INTERNAL_INSECURE_NATIVE_PORT` | `9000` | Native protocol port |

### Authentication

| Variable | Default | Description |
|----------|---------|-------------|
| `CLICKHOUSE_DEFAULT_USER_PASSWORD` | `"changeme123"` | Password for `default` user (use vault in prod) |
| `CLICKHOUSE_ADMIN_USER` | `"default"` | Admin username (use custom to disable `default`) |
| `CLICKHOUSE_ADMIN_PASSWORD` | `""` | Required if `CLICKHOUSE_ADMIN_USER != 'default'` |

### Users & Grants

`CLICKHOUSE_USERS` defines application users with pre-configured grants for common databases:

```yaml
CLICKHOUSE_USERS:
  - name: prod
    password: "{{ vault_prod_password }}"
  - name: stage
    password: "{{ vault_stage_password }}"
```

Each user gets:
- Role `{name}_admin` with `ALL ON *.* WITH GRANT OPTION`
- Grants on specific databases: `system`, `{name}_xapi`, `{name}_xapi_events_all`, `{name}_reporting`, `{name}_event_sink`, `{name}_vector`, `openedx`, `reporting`, `xapi`, `event_sink`
- Permissions: `CREATE USER`, `ALTER USER`, `DROP FUNCTION`, `CREATE FUNCTION`

### Storage & Backup

| Variable | Default | Description |
|----------|---------|-------------|
| `CLICKHOUSE_VOLUMES` | `[]` | EBS volumes for `mount_ebs` role |
| `CLICKHOUSE_BACKUP_DISK_NAME` | `backups` | Backup disk name in ClickHouse |
| `CLICKHOUSE_BACKUP_ROOT` | `/backups/clickhouse` | Backup disk path |
| `CLICKHOUSE_BACKUP_ENABLED` | `false` | Include `clickhouse_backup` role |

### Logging

| Variable | Default | Description |
|----------|---------|-------------|
| `CLICKHOUSE_LOG_LEVEL` | `warning` | Log level (trace, debug, information, warning, error, fatal) |
| `CLICKHOUSE_SYSTEM_LOGS_ENABLED` | `false` | Enable system log tables |
| `CLICKHOUSE_SYSTEM_LOG_TABLES` | (list) | Tables with retention days |

### Custom Configuration

```yaml
CLICKHOUSE_CUSTOM_CONFIGS:
  max_concurrent_queries.xml: |
    <clickhouse>
      <max_concurrent_queries>200</max_concurrent_queries>
    </clickhouse>
  custom_setting.xml: |
    <clickhouse>
      <some_setting>value</some_setting>
    </clickhouse>
```

Files written to `/etc/clickhouse-server/config.d/`.

## Generated Configuration Files

```
/etc/clickhouse-server/
├── config.d/
│   ├── host.xml              # Ports, listen hosts
│   ├── backup_disk.xml       # Backup disk configuration
│   ├── system_logs.xml       # System log tables & TTL
│   └── *.xml                 # Custom configs from CLICKHOUSE_CUSTOM_CONFIGS
├── users.xml                 # Users, profiles, quotas
└── users.d/
    └── remove_default_user.yaml  # Created when custom admin used
```

## Example Playbook

```yaml
- hosts: clickhouse_servers
  become: true
  vars:
    CLICKHOUSE_VERSION: "25.8"
    CLICKHOUSE_DEFAULT_USER_PASSWORD: "{{ vault_clickhouse_default_password }}"
    CLICKHOUSE_ADMIN_USER: "admin"
    CLICKHOUSE_ADMIN_PASSWORD: "{{ vault_clickhouse_admin_password }}"
    CLICKHOUSE_VOLUMES:
      - device: /dev/nvme1n1
        mount: /var/lib/clickhouse
        fstype: ext4
        size: "500 GiB"
      - device: /dev/nvme2n1
        mount: /backups/clickhouse
        fstype: ext4
        size: "200 GiB"
    CLICKHOUSE_BACKUP_ENABLED: true
    CLICKHOUSE_USERS:
      - name: analytics
        password: "{{ vault_analytics_password }}"
  roles:
    - clickhouse
```

## Upgrade Procedure

### Patch/Minor (Automatic)
```bash
# Update CLICKHOUSE_VERSION to new minor (e.g., "25.8" -> "25.11")
ansible-playbook -i inventory clickhouse.yml --tags upgrade
```

### Major (Manual)
1. Run backup: `ansible-playbook -i inventory clickhouse_backup.yml`
2. Set `CLICKHOUSE_ALLOW_MAJOR_UPGRADE: true`
3. Update `CLICKHOUSE_VERSION` (e.g., "25.8" -> "26.1")
4. Run playbook: `ansible-playbook -i inventory clickhouse.yml --tags upgrade`
5. Verify: `clickhouse-client --query "SELECT version()"`

## Tags

| Tag | Tasks |
|-----|-------|
| `validate` | Input validation |
| `install` | Package installation |
| `upgrade` | Version upgrade |
| `configure` | Configuration templates |
| `bootstrap` | Service start, user creation |
| `users` | User/role/grant management |
| `storage` | EBS volume mounting |
| `backup` | Backup role inclusion |
| `clickhouse` | All tasks (umbrella) |

## Molecule Testing

```bash
cd molecule/clickhouse
molecule test
```

Test scenarios:
- Default convergence
- Custom admin user
- Backup enabled
- Custom configs
- Version upgrade

## Troubleshooting

### ClickHouse won't start
- Check logs: `journalctl -u clickhouse-server -f`
- Verify config: `clickhouse-server --config-file=/etc/clickhouse-server/config.xml --check-config`

### Can't connect
- Verify ports: `ss -tlnp | grep -E '8123|9000'`
- Check firewall/security groups

### Upgrade failed
- Check installed version: `clickhouse-server --version`
- Verify repo: `apt-cache policy clickhouse-server`
- Major upgrade requires `CLICKHOUSE_ALLOW_MAJOR_UPGRADE=true`

## License

MIT