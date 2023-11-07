# How to configure the sites: 

## Option 1:

In the file `group_vars>caddy_servers.yml`, and the variable `caddy_sites` add or remove sites. Once this process is done, run: `ansible-playbook caddy.yml -i manifests-<name>/ansible_inventory/hosts.ini` or its respective cronjob again.

## Option 2:

Login to the caddy server, and modify the following file: `/etc/caddy/Caddyfile` adding or removing the sites. Once this process is done, run `caddy reload --config /etc/caddy/Caddyfile`. 
