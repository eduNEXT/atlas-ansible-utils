#!/usr/bin/env bash
# Smoke test for AWS SSM connectivity using test_os_info.yml.
# Usage:
# AWS_PROFILE=<profile> AWS_SSM_BUCKET=<bucket> ./scripts/ssm-smoke-test.sh <instance-id> [inventory-path]
set -euo pipefail

INSTANCE_ID="${1:?Usage: AWS_PROFILE=<profile> AWS_SSM_BUCKET=<bucket> $0 <instance-id> [inventory-path]}"
INVENTORY_PATH="${2:-inventories/examples/ssm/hosts.ini}"
AWS_REGION="${AWS_REGION:-us-west-2}"
AWS_PROFILE_NAME="${AWS_PROFILE:-${AWS_DEFAULT_PROFILE:-}}"
AWS_SSM_BUCKET="${AWS_SSM_BUCKET:-}"
ANSIBLE_REMOTE_TEMP="${ANSIBLE_REMOTE_TEMP:-/tmp/ansible-ssm}"
REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

if [[ -z "${AWS_SSM_BUCKET}" ]]; then
  echo "ERROR: AWS_SSM_BUCKET is required by the amazon.aws.aws_ssm connection plugin." >&2
  echo "Set it to an S3 bucket that the controller profile can read/write/delete." >&2
  exit 1
fi

TMP_INVENTORY="$(mktemp)"
trap 'rm -f "${TMP_INVENTORY}"' EXIT

sed "s/INSTANCE_ID/${INSTANCE_ID}/g" "${REPO_ROOT}/${INVENTORY_PATH}" > "${TMP_INVENTORY}"

cd "${REPO_ROOT}"
make requirements

ANSIBLE_EXTRA_VARS=(
  -e "ansible_aws_ssm_region=${AWS_REGION}"
  -e "ansible_aws_ssm_bucket_name=${AWS_SSM_BUCKET}"
  -e "ansible_remote_tmp=${ANSIBLE_REMOTE_TEMP}"
)
if [[ -n "${AWS_PROFILE_NAME}" ]]; then
  ANSIBLE_EXTRA_VARS+=(-e "ansible_aws_ssm_profile=${AWS_PROFILE_NAME}")
  echo "Using AWS profile: ${AWS_PROFILE_NAME}"
else
  echo "Using default AWS credential provider chain"
fi
echo "Using SSM transfer bucket: ${AWS_SSM_BUCKET}"
echo "Using remote temp path: ${ANSIBLE_REMOTE_TEMP}"

uv run ansible-playbook playbooks/test_os_info.yml \
  -i "${TMP_INVENTORY}" \
  --limit test_hosts \
  "${ANSIBLE_EXTRA_VARS[@]}" \
  -v
