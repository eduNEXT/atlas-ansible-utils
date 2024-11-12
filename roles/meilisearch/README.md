Ansible Role: Meilisearch
=========================

This role installs and configures [MeiliSearch](https://www.meilisearch.com/docs) on Debian/Ubuntu.

Requirements
------------

No special requirements; note that this role requires root access, so either run it in a playbook with a global `become: yes`, or invoke the role in your playbook like:

    - hosts: foobar
      roles:
        - role: meilisearch
          become: yes

Role Variables
--------------

Available variables are listed below, along with default values (see `defaults/main.yml`):

    meilisearch_state: started
    meilisearch_enabled_at_boot: true

Start and enable MeiliSearch at boot.

    meilisearch_user: 'meilisearch'
    meilisearch_group: 'meilisearch'

Configure the user and group to run meilisearch as. **These will be created, so do not use existing users, as they will be modified!**

    meilisearch_exe_path: '/usr/bin/meilisearch'

Configure the path where the binary should be placed.

    meilisearch_db_path: '/var/lib/meilisearch'

Configure the path where the database should be placed.

    meilisearch_listen_ip: 0.0.0.0
    meilisearch_listen_port: 7700

Configure the IP and port on which MeiliSearch should listen.

    meilisearch_master_key: 'Y0urVery-S3cureAp1K3y'

The MeiliSearch master key. **This must be changed for security reasons**. For more information see [this link](https://www.meilisearch.com/docs/learn/self_hosted/configure_meilisearch_at_launch#master-key).

Dependencies
------------

None.

Example Playbook
----------------

    - name: Configure Meilisearch instances
      hosts: meilisearch_servers
      become: true
      gather_facts: true
      roles:
        - role: meilisearch
