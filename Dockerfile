FROM python:3.11-slim-bookworm AS minimal
ARG DEBIAN_FRONTEND=noninteractive

RUN --mount=type=cache,target=/var/cache/apt,sharing=locked \
    --mount=type=cache,target=/var/lib/apt,sharing=locked \
    apt update && \
    apt install -y build-essential git

FROM minimal AS dependencies
ENV VIRTUAL_ENV=/opt/venv
ENV ANSIBLE_HOME=/opt/ansible
RUN python -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

COPY ./requirements/ ./requirements/
RUN --mount=type=cache,mode=0755,target=/root/.cache/pip \
    set -eux; \
    pip install -qr requirements/pip-tools.txt; \
    pip-sync requirements/base.txt

COPY ./requirements.yml .
RUN ansible-galaxy install -r requirements.yml

FROM python:3.11-slim-bookworm AS final

RUN --mount=type=cache,target=/var/cache/apt,sharing=locked \
    --mount=type=cache,target=/var/lib/apt,sharing=locked \
    apt update && \
    apt install -y openssh-client

RUN set -eux; \
    groupadd --system --gid 1000 runner; \
    useradd --system --gid runner --uid 1000 --home-dir /runner runner; \
    mkdir -p /runner; \
    chown -R runner:runner /runner;

ENV VIRTUAL_ENV=/opt/venv
ENV ANSIBLE_HOME=/opt/ansible
ENV ANSIBLE_REMOTE_TEMP=/dev/shm
ENV ANSIBLE_LOCAL_TEMP=/dev/shm
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
COPY --from=dependencies $VIRTUAL_ENV $VIRTUAL_ENV
COPY --from=dependencies $ANSIBLE_HOME $ANSIBLE_HOME

USER 1000:1000

WORKDIR /runner/atlas-ansible-utils
COPY  ./hosts.ini /etc/ansible/
COPY  . .

# For now, we prefer skipping the host key checking
ENV ANSIBLE_HOST_KEY_CHECKING="no"
ENV ATLAS_ANSIBLE_PLAYBOOK="test_os_info.yml"
ENV ATLAS_ANSIBLE_PLAYBOOK_EXTRA_PARAMS=""
ENV ANSIBLE_INVENTORY="/etc/ansible/hosts.ini"

CMD [ "/bin/sh", "-c", "ansible-playbook ${ATLAS_ANSIBLE_PLAYBOOK} ${ATLAS_ANSIBLE_PLAYBOOK_EXTRA_PARAMS}" ]
