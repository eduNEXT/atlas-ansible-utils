#!/usr/bin/env bash
set -e

if [ ! -z "$@" ]; then
	exec $@
fi

exec ansible-playbook "playbooks/$ATLAS_ANSIBLE_PLAYBOOK" ${ATLAS_ANSIBLE_PLAYBOOK_EXTRA_PARAMS}
