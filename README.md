# Atlas Ansible Utils

This repository contains a collection of Ansible roles and playbooks used to deploy different services in the OpenedX platform context. Although the adoption of containerized application platforms like Kubernetes by the OpenedX community, there are special case where Ansible tools are still required, for instance, to deploy databases in on-premises.

Versioning
----------

This repository follows the same versioning scheme as the Tutor project, where each major version maps to an Open edX release. For each release we provide the ansible scripts needed to provision the databases used by an Open edX instance on said release.


| Open edX release | Tutor version     | Atlas Ansible Utils version |
|------------------|-------------------|-----------------------------|
| Quince and older | `<18`             | 1.11.0                      |
| Redwood          | `>=18.0, <19`     | >=18.0.0                    |

The following is the list of supported operating systems.

| Playbook           | Ubuntu 22.04 | Ubuntu 24.04 |
|--------------------|--------------|--------------|
| redis_7            |      x       |       x      |
| mysql_8_4          |      x       |       x      |
| mongo_7_0          |      x       |       x      |
| elasticsearch_7    |      x       |       x      |
| clickhouse         |      x       |              |

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
    ansible-playbook playbooks/mysql_5_7.yml -i ../your-inventory-repo/path/to/hosts.ini -v

Full options for **ansible-playbook** command can be found [here](https://docs.ansible.com/ansible/latest/cli/ansible-playbook.html)

---

## Using the Docker image

This repo contains a Dockerfile that can be used to build a Docker image with all the requirements and run the playbooks. To run the image, run the following command:

    docker run --rm -it ednxops/atlas-ansible-utils:<tagname>

When this command is executed:

- No additional parameters are provided on the command line. Therefore, the default values defined in the Dockerfile and the image will be used.

- The environment variable **ATLAS_ANSIBLE_PLAYBOOK** is set to "test_os_info.yml" by default which is used for testing purposes **ONLY**, helps verify that the ansible-playbook binary can run playbooks as expected..

- The environment variable **ATLAS_ANSIBLE_PLAYBOOK_EXTRA_PARAMS** is set to an empty string by default, which means no additional parameters will be added to the ansible-playbook command.

- **--rm** flag is used to remove the container when it exits after running the command.

Use other command line parameters to override the default values. For example:

    docker run --rm -it -v "/your/local/path/ssh-key/id_key:/app/.ssh/id_rsa" -v "/your/local/path/inventory:/app/inventory" -e "ATLAS_ANSIBLE_PLAYBOOK=mysql_5_7.yml" -e "ATLAS_ANSIBLE_PLAYBOOK_EXTRA_PARAMS=-i /app/inventory/hosts.ini -u ubuntu -v" ednxops/atlas-ansible-utils:<tagname>

In this case, we can override the default variables using:

- When this command is executed, it mounts the private SSH key file id_key from the directory **/your/local/path/ssh-key** on the host to the container at the location **/app/.ssh/id_rsa**. It also mounts the inventory directory from **/your/local/path//inventory** on the host to **/app/inventory** in the container.

> **_NOTE:_** SSH credentials can be shared in any path on the docker container using the **ANSIBLE_PRIVATE_KEY_FILE** environment variable which allows to define the path where SSH credentials are located.

- The environment variable **ATLAS_ANSIBLE_PLAYBOOK_EXTRA_PARAMS** is set to **"-i /app/inventory/hosts.ini -u ubuntu -v"**, which adds additional parameters to the ansible-playbook command. These parameters specify the inventory file, remote user, and verbose mode for Ansible.

- The **-u** flag is used to set the user to connect to the target machines. In this case, the user is **ubuntu**.

---

## Using in Kubernetes

To run the atlas-ansible-utils playbooks to provision external servers from Kubernetes, jobs or cronjobs can be implemented using the atlas-ansible-utils Docker image. Let's look at the following example:

    apiVersion: batch/v1
    kind: Job
    metadata:
      name: ansible-playbook-mysql-job
      namespace: "tokio-openedx"
    spec:
      template:
        spec:
          securityContext:
            fsGroup: 1000
          containers:
          - name: ansible-runner
            image: ednxops/atlas-ansible-utils:1.1.0
            env:
            - name: ATLAS_ANSIBLE_PLAYBOOK
              value: "mysql_5_7.yml"
            - name: ATLAS_ANSIBLE_PLAYBOOK_EXTRA_PARAMS
              value: "-i /git/manifests/manifests-yamato.git/ansible_inventory/hosts -u ubuntu -v"
            - name: ANSIBLE_PRIVATE_KEY_FILE
              value: "/tmp/extra-ssh-keys/id-rsa"
            volumeMounts:
            - mountPath: /git
              name: inventory-content
            - mountPath: /tmp/extra-ssh-keys
              readOnly: true
              name: sshdir
          initContainers:
          - name: inventory-git-sync
            image: registry.k8s.io/git-sync/git-sync:v4.0.0
            volumeMounts:
            - mountPath: /git
              name: inventory-content
            - mountPath: /tmp/extra-ssh-keys
              readOnly: true
              name: sshdir
            env:
            - name: GITSYNC_MAX_FAILURES
              value: "3"
            - name: GITSYNC_ONE_TIME
              value: "true"
            - name: GITSYNC_REF
              value: "mar/test-provisioning-db"
            - name: GITSYNC_REPO
              value: "git@github.com:eduNEXT/manifests-yamato.git"
            - name: GITSYNC_ROOT
              value: "/git/manifests"
            - name: GITSYNC_SSH
              value: "true"
            - name: GITSYNC_SSH_KEY_FILE
              value: "/tmp/extra-ssh-keys/id-rsa"
            - name: GITSYNC_SSH_KNOWN_HOSTS
              value: "false"
          volumes:
          - name: inventory-content
            emptyDir: {}
          - name: sshdir
            secret:
              secretName: ssh-github
              items:
              - key: ssh-privatekey
                path: id-rsa
          restartPolicy: Never
      backoffLimit: 4

This job has the following features:

- It mounts a secret called **ssh-github** in a volume. Such secret should contain the ssh credentials to connect to the Ansible external target servers, as well as to fetch the inventory repository. For convenience, such credentials are the same for both, servers access and repository cloning. The secret can be creates with the command:

      kubectl create secret generic ssh-github --from-file=path/to/you/ssh-private-key

or you can create it via ArgoCD.

- There's a single initContainer whose unique function is to fetch the inventory repository. It uses the [gitsync tool](https://github.com/kubernetes/git-sync) to do so.

- The **atlas-ansible-utils** image is used in the main pod container to execute the desired ansible-playbook in the target servers, mounting the ssh-key and the inventory repository as volumes. The configuration is defined through environment variables.

---

**NOTE**

For now this repo supports the playbooks for:
- MySQL 5.7
- Mongo 4.2
- Percona 5.7
- Caddy

---
## Extract and Restore databases:

The procedure involves extracting specific databases, creating backups of each, and subsequently restoring them into a new database. A list of databases to process will be compiled, and for each, a backup will be created followed by a restoration. The outcome will be a new database named after the original with an appended suffix. For example, if the original database is named `edxapp`, the new database will be called `edxapp_clone`, containing the data from the original database.

This process will be carried out using the `admin` user for MySQL and Mongo, which must have the necessary permissions to perform these operations.

### Launching Database Restoration:

1. Install atlas-ansible-utils following [these instructions](https://github.com/eduNEXT/atlas-ansible-utils?tab=readme-ov-file#how-to-use-this-repo).
2. Configure the variables that the roles mysql_clone and mongo_clone need to work.

  #### How to set variables to clone:

  ##### MySQL
  The variables that you must configure in [defaults.yml](https://github.com/eduNEXT/atlas-ansible-utils/blob/main/roles/mysql_clone/defaults/main.yml) are:

  - `MYSQL_CLONE_USER`: User with the necessary privileges to perform backups and restore databases.
  - `MYSQL_CLONE_PASSWORD`: Password of this user.
  - `MYSQL_CLONE_DB_LIST`: List of databases you wish to clone.
  - `MYSQL_CLONE_TARGET_PATH`: Path where the database is mounted to check available space.

    The variable configuration should look like this:
    ```yaml
      MYSQL_CLONE_USER: admin
      MYSQL_CLONE_PASSWORD: ABCDefgh12345
      MYSQL_CLONE_TARGET_PATH: /var/lib/mysql
      MYSQL_CLONE_DB_LIST:
      - edxapp
      - edx_notes_api

      # Other variables...
    ```
  ##### MongoDB
  Similar to the MySQL configuration, the variables that you must configure in [defaults.yml](https://github.com/eduNEXT/atlas-ansible-utils/blob/main/roles/mongo_clone/defaults/main.yml) are:

  - `MONGO_CLONE_USER`: User with the necessary privileges to perform backups and restore databases.
  - `MONGO_CLONE_PASSWORD`: Password of this user.
  - `MONGO_CLONE_DB_LIST`: List of databases you wish to clone.
  - `MONGO_CLONE_TARGET_PATH`: Path where the database is mounted to check available space.

    The variable configuration should look like this:
      ```yaml
        MONGO_CLONE_USER: admin
        MONGO_CLONE_PASSWORD: ABCDefgh12345
        MONGO_CLONE_TARGET_PATH: /edx/var/mongo/mongodb
        MONGO_CLONE_DB_LIST:
        - edxapp
        - cs_comments_service

        # Other variables...
      ```
3. Execute the routine to restore the databases:

  For mongo:

   ```bash
   ansible-playbook playbooks/mongo_backup_restore.yml -i /path/inventory/host.ini -v
   ```

  For mongo:

   ```bash
   ansible-playbook playbooks/mysql_backup_restore.yml -i /path/inventory/host.ini -v
   ```

Upon completion of the execution, you should observe both the existing databases and the new databases suffixed with `_clone` in your database instance, as per the default configuration.

## Molecule tests

Integration testing is performed using [molecule](https://ansible.readthedocs.io/projects/molecule/).

Molecule tests consist of different scenarios which are implemented using ansible roles, those are run on Docker and
can be customized per role.

### Getting started

Install molecule via:

```shell
pip install molecule[docker] ansible-lint
```

### Run tests

A test consist of the following phases:

- **create**: Create a docker instance for the scenario to test. See `molecule/**/molecule.yml` for examples.
- **converge**: Create a docker instance for the scenario to test and runs the role specified on `molecule/**/converge.yml`
- **verify**: After the `converge` phase, you can run the `verify` command to check wheter your role was succesfully run.
  See `molecule/**/verify.yml` for examples.
- **idempotence**: After the `converge` phase, you can run the `idempotence` command to check if your role is idempotent.
- **destroy**: Destroys the created docker instance for the scenario.

You can run a whole scenario by running:

```shell
molecule test -s scenario_name
```

You can also run the steps independently using the following commands:

```shell
molecule create -s scenario_name
molecule converge -s scenario_name
molecule verify -s scenario_name
molecule idempotence -s scenario_name
molecule destroy -s scenario_name
```

To debug molecule tests you can run the converge phase and login to the docker instance:

```shell
molecule converge -s scenario_name
molecule login -s scenario_name
```

See [molecule documentation](https://ansible.readthedocs.io/projects/molecule/) for more information.
