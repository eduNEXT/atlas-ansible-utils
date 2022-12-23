# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased](https://github.com/eduNEXT/atlas-ansible-utils/compare/1.0.0...HEAD)

Please do not update the unreleased notes.

<!-- Content should be placed here -->
## [1.0.0](https://github.com/eduNEXT/atlas-ansible-utils/compare/0.1.0...1.0.0) - 2022-10-27

### Features

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

### Code Refactoring

- Update requirements to use Pymongo.
- Update cache before installing python3-pip.
- Use a new variable in the mysql_config role to control where to store the custom MySQL configuration files.
- Updating requirements.

### Bug fixes

- Add missing bracket in jinja template.
- Fixing a couple of issues with Mongo and MySQL roles.
- Create Mongo DBs when using a standalone installation to avoid connection failures.
- Move percona role under the proper key in requirements file.

## [0.1.0] - 2022-10-27

### Added

- First release on GitHub before being a stable library.
