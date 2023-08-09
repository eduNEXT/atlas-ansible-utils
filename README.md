# Atlas Ansible Utils

This repository contains a collection of Ansible roles and playbooks used to deploy different services in the OpenedX platform context. Although the adoption of containerized application platforms like Kubernetes by the OpenedX community, there are special case where Ansible tools are still required, for instance, to deploy databases in on-premises.

## How to use this repo

In most cases, this repo is used from **command and control** instance (Ubuntu 20.04 or later versions) to provision target machines. Before using this repo in the CNC machine, verify that:

- CNC runs Python 3.8 or a later version (3.8 recommended)
- You have SSH connectivity between the CNC instances and the machines you want to provision
- You have an Ansible inventory with configuration variables (check section below)

Additionally, run the commands below to prepare the CNC:

    sudo apt update
    sudo apt install -y python3-pip
    pip3 install virtualenv

### Ansible inventory

This is a set of files that defines configuration variables for machines provision. For instance, the number of workers a service will deploy or the list of users to create in a database are configuration variables. A simplified version of an inventory folder structure is presented below:

```
environment
│   hosts.ini
└───group_vars
       all.yaml
```

Inventory is generally separated per environment, and contains a **hosts** file (hosts.ini including target hosts to provision) and a **group_vars** folder which can contain multiple files in yaml format. These files contain configuration variables. For simplicity, we store our variables in a file called **all.yaml**. Important to mention that inventories can get as complicated as the use case requires. Please visit [Ansible docs page](https://docs.ansible.com/ansible/latest/user_guide/intro_inventory.html) to get further information about inventories.

> **_NOTE:_** Generally our inventories are included in the manifest repositories. There you can find examples on how to create a new inventory.

### Running a playbook

Let's say we want to provision a machine to run MySQL, so we run the following in the CNC machine:

    mkdir -p db_ops && cd db_ops
    git clone git@github.com:eduNEXT/atlas-ansible-utils.git
    git clone git@github.com:eduNEXT/your-inventory-repo.git
    virtualenv venv
    source venv/bin/activate
    cd atlas-ansible-utils/
    make requirements
    ansible-playbook mysql_5_7.yml -i ../your-inventory-repo/path/to/hosts.ini -v

Full options for **ansible-playbook** command can be found [here](https://docs.ansible.com/ansible/latest/cli/ansible-playbook.html)

---

## Use docker image

This repo contains a Dockerfile that can be used to build a docker image with all the requirements to run the playbooks. To build the image, run the following command:

    docker run --rm -it atlas-ansible-util:1.0.0

When this command is executed:

No additional parameters are provided on the command line. Therefore, the default values defined in the Dockerfile and the image will be used.

The environment variable **ATLAS_ANSIBLE_PLAYBOOK** is set to "test_os_info.yml" by default which is used for testing purposes **ONLY**, helps verify that the ansible-playbook binary can run playbooks as expected..

The environment variable **ATLAS_ANSIBLE_PLAYBOOK_EXTRA_PARAMS** is set to an empty string by default, which means no additional parameters will be added to the ansible-playbook command.



    docker run --rm -it -v "/your/local/path/ssh-key/id_key:/app/.ssh/id_rsa" -v "/your/local/path/inventory:/app/inventory" -e "ATLAS_ANSIBLE_PLAYBOOK=mysql_5_7.yml" -e "ATLAS_ANSIBLE_PLAYBOOK_EXTRA_PARAMS=-i /app/inventory/hosts.ini -u ubuntu -v" atlas-ansible-utils:1.0.0

The command above will run the playbook **mysql_5_7.yml** using the inventory file **hosts.ini** and the user **ubuntu**. The SSH key is mounted in the container to allow the connection to the target machine.

---
**NOTE**

For now this repo supports the playbooks for:
- MySQL 5.7
- Mongo 4.2
- Percona 5.7
---
