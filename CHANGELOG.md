# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased](https://github.com/eduNEXT/atlas-ansible-utils/compare/v1.4.0...HEAD)

Please do not update the unreleased notes.

<!-- Content should be placed here -->
## [v1.4.0](https://github.com/eduNEXT/atlas-ansible-utils/compare/v1.3.0...v1.4.0) - 2023-11-07

### [1.4.0](https://github.com/eduNEXT/atlas-ansible-utils/compare/v1.3.0...v1.4.0) (2023-11-07)

#### Features

- add playbooks to provision ClickHOuse ([#17](https://github.com/eduNEXT/atlas-ansible-utils/issues/17)) ([31b15b2](https://github.com/eduNEXT/atlas-ansible-utils/commit/31b15b21a10170099cd10a52ac453471d539fdb3))

## [v1.3.0](https://github.com/eduNEXT/atlas-ansible-utils/compare/v1.2.0...v1.3.0) - 2023-10-09

### [1.3.0](https://github.com/eduNEXT/atlas-ansible-utils/compare/v1.2.0...v1.3.0) (2023-10-09)

#### Features

- add mysql8.0 and mongo4.4 playbooks ([#13](https://github.com/eduNEXT/atlas-ansible-utils/issues/13)) ([33184f0](https://github.com/eduNEXT/atlas-ansible-utils/commit/33184f01195b91202ae858b39d4a2dff5b751545))

## [v1.2.0](https://github.com/eduNEXT/atlas-ansible-utils/compare/v1.1.0...v1.2.0) - 2023-10-02

### [1.2.0](https://github.com/eduNEXT/atlas-ansible-utils/compare/v1.1.0...v1.2.0) (2023-10-02)

#### Features

- add backup ansible playbooks ([#11](https://github.com/eduNEXT/atlas-ansible-utils/issues/11)) ([3f7433f](https://github.com/eduNEXT/atlas-ansible-utils/commit/3f7433f7c7aba0aeb1573d7e8d8164bf8a0d0104))

## [v1.1.0](https://github.com/eduNEXT/atlas-ansible-utils/compare/1.0.0...v1.1.0) - 2023-08-25

### [1.1.0](https://github.com/eduNEXT/atlas-ansible-utils/compare/v1.0.0...v1.1.0) (2023-08-25)

#### Features

- add releases for docker image ([#7](https://github.com/eduNEXT/atlas-ansible-utils/issues/7)) ([d069421](https://github.com/eduNEXT/atlas-ansible-utils/commit/d069421a78e7beb85ef3227e2ad880f146cbe139))

#### Bug Fixes

- update package cache when installing dependencies ([#9](https://github.com/eduNEXT/atlas-ansible-utils/issues/9)) ([2b55913](https://github.com/eduNEXT/atlas-ansible-utils/commit/2b559130fb5559ca744b2e8f15b98170a394c55f))

#### Documentation

- updating readme ([a99e098](https://github.com/eduNEXT/atlas-ansible-utils/commit/a99e098773cfc0de21cf75f25c17133547da926a))

## [1.0.0](https://github.com/eduNEXT/atlas-ansible-utils/compare/0.1.0...1.0.0) - 2022-10-27

### [1.0.0](https://github.com/eduNEXT/atlas-ansible-utils/compare/0.1.0...1.0.0) (2022-10-27)

#### Features

- Adding generic Ansible configuration generated with "$ ansible-config init --disabled > ansible.cfg".
- Adding MySQL role just to install MySQL Inspired on openedx-configuration MySQL role.
- Adding role to configure MySQL installation.
- Adding main MySQL 5.7 playbook.
- Adding mongo 4.2 role and other main roles.
- Adding custom modules required by Mongo 4.2 role.
- Adding main Mongo 4.2 playbook.
- Adding role to mount volumes in MySQL and Mongo roles.
- Adding support to define MySQL server charset and collation.
- Adding first version of Percona 5.7 playbook.
- Adding playbook to deploy Percona database in specific hosts.
- Adding support for machine hostnames.

#### Code Refactoring

- Update requirements to use Pymongo.
- Update cache before installing python3-pip.
- Use a new variable in the mysql_config role to control where to store the custom MySQL configuration files.
- Updating requirements.

#### Bug fixes

- Add missing bracket in jinja template.
- Fixing a couple of issues with Mongo and MySQL roles.
- Create Mongo DBs when using a standalone installation to avoid connection failures.
- Move percona role under the proper key in requirements file.

## [0.1.0](https://github.com/eduNEXT/atlas-ansible-utils/commits/0.1.0) - 2022-10-27

### [0.1.0](https://github.com/eduNEXT/atlas-ansible-utils/commits/0.1.0) (2022-10-27)

#### Features

- First release on GitHub before being a stable library.
