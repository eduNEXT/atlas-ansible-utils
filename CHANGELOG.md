# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased](https://github.com/eduNEXT/atlas-ansible-utils/compare/1.0.0...HEAD)

Please do not update the unreleased notes.

<!-- Content should be placed here -->

## [1.0.0](https://github.com/eduNEXT/atlas-ansible-utils/compare/0.1.0...1.0.0) - 2022-10-27

### Added

- Generic Ansible configuration generated with "$ ansible-config init --disabled > ansible.cfg".
- MySQL role just to install MySQL Inspired on openedx-configuration MySQL role.
- Role to configure MySQL installation.
- Main MySQL 5.7 playbook.
- Mongo 4.2 role and other main roles.
- Custom modules required by Mongo 4.2 role.
- Main Mongo 4.2 playbook.
- Role to mount volumes in MySQL and Mongo roles.
- Support to define MySQL server charset and collation.
- First version of Percona 5.7 playbook.
- Playbook to deploy Percona database in specific hosts.
- Support for machine hostnames.

### Changed

- Updating requirements.
- Add a new variable in the mysql_config role to control where to store the custom MySQL configuration files.
- Update cache before installing python3-pip.
- Update requirements to use Pymongo.

### Fixed

- Move percona role under the proper key in requirements file.
- Create Mongo DBs when using a standalone installation to avoid connection failures.
- Fixing a couple of issues with Mongo and MySQL roles.
- Add missing bracket in jinja template.


## [0.1.0] - 2022-10-27

### Added

- First release on GitHub before being a stable library.
