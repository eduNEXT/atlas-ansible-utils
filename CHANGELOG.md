# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## v20.0.0 (2025-11-13)

### Features

- Teak support (#67) ([`bf24c45`](https://github.com/eduNEXT/atlas-ansible-utils/commit/bf24c45af076df8ff7712b0c9c7e0a144ae582f0))

## v19.1.0 (2025-10-22)

### Features

- Updated task to get clickhouse gpg key (#65) ([`25ef313`](https://github.com/eduNEXT/atlas-ansible-utils/commit/25ef3132ebab1fa9900b66f989859d4036ca91ed))

## v19.0.1 (2025-08-01)

### Bug fixes

- Added ignore to pep 668 in backups playbooks (#61) ([`b34c18d`](https://github.com/eduNEXT/atlas-ansible-utils/commit/b34c18dae55dd062337c67fa30a5af74ade479ab))

## v19.0.0 (2024-12-18)

### Features

- Sumac support (#57) ([`d8dafcf`](https://github.com/eduNEXT/atlas-ansible-utils/commit/d8dafcf3084fb1fa4743c191882fd38845e1d6b4))

## v18.2.1 (2024-11-29)

### Bug fixes

- Use ip hash as load balancing algorithm (#60) ([`f6ce39c`](https://github.com/eduNEXT/atlas-ansible-utils/commit/f6ce39c98608a6cbb54556bc3a28b9a24bc08609))

## v18.2.0 (2024-11-29)

### Features

- Add haproxy docker role (#59) ([`38148de`](https://github.com/eduNEXT/atlas-ansible-utils/commit/38148de738adf4de262047e0cc803becd852b773))
- Use a custom network for docker databases (#55) ([`ace0b76`](https://github.com/eduNEXT/atlas-ansible-utils/commit/ace0b767973eb7a0353222e81763773a4a51b4c3))

## v18.1.0 (2024-11-25)

### Features

- Add caddy health checks (#58) ([`e9b267d`](https://github.com/eduNEXT/atlas-ansible-utils/commit/e9b267dd7365cd2bf6e1c76a9898961343f3610d))

## v18.0.1 (2024-11-07)

### Bug fixes

- Removing galaxy dependencies (#56) ([`b89eb61`](https://github.com/eduNEXT/atlas-ansible-utils/commit/b89eb6141c862319a96f2fb1953da6f2a7b0e48d))

## v18.0.0 (2024-10-08)

### Features

- Add support for ubuntu24 for mongo 7.0 (#52) ([`826f088`](https://github.com/eduNEXT/atlas-ansible-utils/commit/826f0887b442919065f80ead18bd1248a5851f07))
- Add support to clickhouse for ubuntu 24 (#48) ([`5637a7b`](https://github.com/eduNEXT/atlas-ansible-utils/commit/5637a7bc610e8049241b266fc9f1a45b3d894fae))
- Add support to redis for ubuntu 24 (#50) ([`c2a9e61`](https://github.com/eduNEXT/atlas-ansible-utils/commit/c2a9e61899e646b1e0e0fb0e71df5bf8133c3d5f))
- Add support to mysql8.4 for ubuntu 24.04 (#47) ([`a7d93f5`](https://github.com/eduNEXT/atlas-ansible-utils/commit/a7d93f5382fbc5f9141b1c3e943903535fbde366))
- Add support to elasticsearch for ubuntu 24 (#49) ([`acb5d19`](https://github.com/eduNEXT/atlas-ansible-utils/commit/acb5d19f74f597a0c1de71fbafec6f496d4810b6))
- Remove older playbooks and roles (#51) ([`d54f78c`](https://github.com/eduNEXT/atlas-ansible-utils/commit/d54f78cfb0cfc0a7826ae14440fd55e0d11e9291))

## v1.11.0 (2024-09-05)

### Features

- Add routine to deploy dbs in docker (#45) ([`b172c2e`](https://github.com/eduNEXT/atlas-ansible-utils/commit/b172c2eba0d9dd83cd59002fee43f7e0097c09a1))

## v1.10.0 (2024-08-22)

### Features

- Add a helmchart to run the playbooks on k8s (#42) ([`b86fd0e`](https://github.com/eduNEXT/atlas-ansible-utils/commit/b86fd0efeca08d1511d0bb5b6b48a071bb71d96b))

## v1.9.0 (2024-07-17)

### Bug fixes

- Disable protected mode in redis 7.2 (#41) ([`3919e5e`](https://github.com/eduNEXT/atlas-ansible-utils/commit/3919e5e3be06f5b14021340f9a21e48e7938606c))

### Features

- Add redis 7.2 playbook (#40) ([`0c4ce6f`](https://github.com/eduNEXT/atlas-ansible-utils/commit/0c4ce6fe1d88b134ab390d43fe35038a60eacbd9))
- Setup ansible lint (#37) ([`1e38950`](https://github.com/eduNEXT/atlas-ansible-utils/commit/1e38950a1111e86ab72c4ae3659785689dcdbe95))
- Upgrade to python 3.11 (#36) ([`7cdca0b`](https://github.com/eduNEXT/atlas-ansible-utils/commit/7cdca0b2232c231ec54d5259986d17c162286050))
- Create playbook to install mysql8.4 (#33) ([`bd3bcdb`](https://github.com/eduNEXT/atlas-ansible-utils/commit/bd3bcdbbff76657b83bba47bc47ff529196375d9))
- Add mongo 7.0 support (#31) ([`3cfa344`](https://github.com/eduNEXT/atlas-ansible-utils/commit/3cfa344c829be4564732b2dc9771bea7f88d09fc))

## v1.8.0 (2024-05-07)

### Bug fixes

- Use default auth plugin in mysql8 (#29) ([`517f8d3`](https://github.com/eduNEXT/atlas-ansible-utils/commit/517f8d3c13eab1b78df97822ffc90815ef7e0e96))
- Verify that the content of the variable defining the suffix contains characters (#27) ([`2d58400`](https://github.com/eduNEXT/atlas-ansible-utils/commit/2d584007cb79dc5f262ccf2c41de0ff34c98fdec))
- Include the --drop flag to delete the destination database before the restore mongo (#26) ([`aa0b02f`](https://github.com/eduNEXT/atlas-ansible-utils/commit/aa0b02fc3553806e760b3f8d88b88c3b30e45cbd))

### Features

- Add gpg in mysql dependencies (#28) ([`eb03b97`](https://github.com/eduNEXT/atlas-ansible-utils/commit/eb03b9704bda89a5eac2bb32cca9ada435d72cfb))

## v1.7.0 (2024-04-03)

### Features

- Add support for restore dbs (#25) ([`3bc5fa7`](https://github.com/eduNEXT/atlas-ansible-utils/commit/3bc5fa77a4859234e25a75bb41f952c91fe8997f))

## v1.6.3 (2024-02-06)

### Bug fixes

- Update mysql repo apt key (#24) ([`fa6d4dc`](https://github.com/eduNEXT/atlas-ansible-utils/commit/fa6d4dc66251cc1c8744c6d5df6ab15a5de72421))

## v1.6.2 (2024-01-17)

### Bug fixes

- Set maxmemory-policy to allkeys-lru (#23) ([`c9798c2`](https://github.com/eduNEXT/atlas-ansible-utils/commit/c9798c20a126ce47b8a0790390fdb8ec7ba3bf5e))
- Add variables in elasticsearch template (#21) ([`6de8d0a`](https://github.com/eduNEXT/atlas-ansible-utils/commit/6de8d0aec593f647cf6f9fd3b807fe1b05105491))

## v1.6.1 (2023-11-22)

### Bug fixes

- Process to restart/reload caddy (#20) ([`994de2f`](https://github.com/eduNEXT/atlas-ansible-utils/commit/994de2f326faa177b84a3cdd0db62019458e2db8))

## v1.6.0 (2023-11-16)

### Features

- Add azstorage for backups (#19) ([`f41286b`](https://github.com/eduNEXT/atlas-ansible-utils/commit/f41286bb023fd048d0e21eea64d4f0781ce7c5d3))

## v1.5.0 (2023-11-09)

### Features

- Redis role (#15) ([`a13fc51`](https://github.com/eduNEXT/atlas-ansible-utils/commit/a13fc51946e8c91ce6f82b7d094abab5bc9a91fd))
- Elasticsearch role (#14) ([`3beea01`](https://github.com/eduNEXT/atlas-ansible-utils/commit/3beea01bdee0faf5ed24dba37c273b394cddf50e))
- Caddy files (#16) ([`27d963a`](https://github.com/eduNEXT/atlas-ansible-utils/commit/27d963a3e6cf33b8ee088faf1a34e0e4489d0df7))

## v1.4.0 (2023-11-07)

### Features

- Add playbooks to provision clickhouse (#17) ([`31b15b2`](https://github.com/eduNEXT/atlas-ansible-utils/commit/31b15b21a10170099cd10a52ac453471d539fdb3))

## v1.3.0 (2023-10-09)

### Features

- Add mysql8.0 and mongo4.4 playbooks (#13) ([`33184f0`](https://github.com/eduNEXT/atlas-ansible-utils/commit/33184f01195b91202ae858b39d4a2dff5b751545))

## v1.2.0 (2023-10-02)

### Features

- Add backup ansible playbooks (#11) ([`3f7433f`](https://github.com/eduNEXT/atlas-ansible-utils/commit/3f7433f7c7aba0aeb1573d7e8d8164bf8a0d0104))

## v1.1.0 (2023-08-25)

### Bug fixes

- Update package cache when installing dependencies (#9) ([`2b55913`](https://github.com/eduNEXT/atlas-ansible-utils/commit/2b559130fb5559ca744b2e8f15b98170a394c55f))

### Features

- Add releases for docker image (#7) ([`d069421`](https://github.com/eduNEXT/atlas-ansible-utils/commit/d069421a78e7beb85ef3227e2ad880f146cbe139))

## v1.0.0 (2022-12-30)

### Bug fixes

- Adding percona role under the proper key in requirements file ([`cc50909`](https://github.com/eduNEXT/atlas-ansible-utils/commit/cc50909ce979ef80405b001e26d03ad2a6cbb9c8))
- Creating mongo dbs when using a standalone installation ([`62ad5ab`](https://github.com/eduNEXT/atlas-ansible-utils/commit/62ad5abae31b3a469b76ee02f6f5aae9ca056e43))
- Templating error ([`d458cf9`](https://github.com/eduNEXT/atlas-ansible-utils/commit/d458cf9f7eba7a1b767a7f626967c6d593174eb6))

### Features

- Adding support for machine hostnames ([`6f7e680`](https://github.com/eduNEXT/atlas-ansible-utils/commit/6f7e6809762b4aa5e2be2bfb7c1e9c6e7d7f7b7e))
- Adding first version of percona 5.7 playbook ([`4f4b756`](https://github.com/eduNEXT/atlas-ansible-utils/commit/4f4b7560ec3db7c1ab307f555425f0c9095b317b))
- Adding support to define mysql server charset and collation ([`00b500d`](https://github.com/eduNEXT/atlas-ansible-utils/commit/00b500d9833f44443ceaf3d9ebd13be2d583186c))
- Updating cache before installing python3-pip ([`7ed1408`](https://github.com/eduNEXT/atlas-ansible-utils/commit/7ed14082957dfb9ff3622caacfd7f78a07939c81))
- Adding role to mount volumes in mysql and mongo roles ([`824db80`](https://github.com/eduNEXT/atlas-ansible-utils/commit/824db8019c8849251d3071a929f69ae307c650c2))
- Fixing a couple of issues with mongo and mysql roles ([`91e9b20`](https://github.com/eduNEXT/atlas-ansible-utils/commit/91e9b208721a7d2926a5e736e9f2d1332c1e7b51))
- Adding main mongo 4.2 playbook ([`e691751`](https://github.com/eduNEXT/atlas-ansible-utils/commit/e69175144968a5364e451c69fc9e0922c714be52))
- Updating requirements to use pymongo ([`b42f225`](https://github.com/eduNEXT/atlas-ansible-utils/commit/b42f225a43788cb95ef4e23cdbb4a36beb49cae2))
- Adding custom modules required by mongo 4.2 role ([`0ab6ed5`](https://github.com/eduNEXT/atlas-ansible-utils/commit/0ab6ed5c45742d482e427ba6f423cbf2bfe562c4))
- Adding mongo 4.2 role ([`9aadacb`](https://github.com/eduNEXT/atlas-ansible-utils/commit/9aadacbf875480c578161323184332f94be355bb))
- Adding basic common roles ([`6fc25c8`](https://github.com/eduNEXT/atlas-ansible-utils/commit/6fc25c8b964308c816f1f4851797d58f6081b53f))
- Adding main mysql 5.7 playbook ([`aa782ec`](https://github.com/eduNEXT/atlas-ansible-utils/commit/aa782ecf80432ea88a6f0c4e8dd9554f8e979ba0))
- Adding role to configure mysql installation ([`b6f0c31`](https://github.com/eduNEXT/atlas-ansible-utils/commit/b6f0c31ed86941ea640a2a21fd1c97179c8f3419))
- Adding mysql role just to install mysql ([`cdf31aa`](https://github.com/eduNEXT/atlas-ansible-utils/commit/cdf31aa84a4703462c05ef5be32ebac2819aaae6))
- Adding generic ansible configuration ([`73e5274`](https://github.com/eduNEXT/atlas-ansible-utils/commit/73e5274bf2ea40459647cf8dcf45f9a3f4a10218))

### Refactoring

- Use standard changelog file with repo changes (#2) ([`402fa0b`](https://github.com/eduNEXT/atlas-ansible-utils/commit/402fa0b126084370e4357b75a62de1eed7a64fa5))

## v1.1.0 (2023-08-25)

### Feature

- Add releases for docker image ([#7](https://github.com/eduNEXT/atlas-ansible-utils/issues/7)) ([d069421](https://github.com/eduNEXT/atlas-ansible-utils/commit/d069421a78e7beb85ef3227e2ad880f146cbe139))

### Fix

- Update package cache when installing dependencies ([#9](https://github.com/eduNEXT/atlas-ansible-utils/issues/9)) ([2b55913](https://github.com/eduNEXT/atlas-ansible-utils/commit/2b559130fb5559ca744b2e8f15b98170a394c55f))

## v1.0.0 (2022-10-27)

### Feature

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

### Refactor

- Update requirements to use Pymongo.
- Update cache before installing python3-pip.
- Use a new variable in the mysql_config role to control where to store the custom MySQL configuration files.
- Updating requirements.

### Fix

- Add missing bracket in jinja template.
- Fixing a couple of issues with Mongo and MySQL roles.
- Create Mongo DBs when using a standalone installation to avoid connection failures.
- Move percona role under the proper key in requirements file.

## v0.1.0 (2022-10-27)

### Feature

- First release on GitHub before being a stable library.
