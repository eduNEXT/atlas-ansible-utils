FROM docker.io/ubuntu:22.04

ARG DEBIAN_FRONTEND=noninteractive

RUN apt update && \
  apt upgrade -y && \
  apt install -y software-properties-common && \
  add-apt-repository ppa:deadsnakes/ppa

RUN apt install -y git python3.11 python3-pip python3.11-distutils make python-is-python3 && \
  rm -rf /var/lib/apt/lists/*

ARG APP_USER_ID=1000
RUN useradd --home-dir /app --create-home --shell /bin/bash --uid ${APP_USER_ID} app
USER ${APP_USER_ID}

COPY --chown=${APP_USER_ID}:${APP_USER_ID} . /app/atlas-ansible-utils/
WORKDIR /app/atlas-ansible-utils

ENV PATH /app/.local/bin:${PATH}
RUN make requirements

# For now, we prefer skipping the host key checking
ENV ANSIBLE_HOST_KEY_CHECKING "no"
ENV ATLAS_ANSIBLE_PLAYBOOK "test_os_info.yml"
ENV ATLAS_ANSIBLE_PLAYBOOK_EXTRA_PARAMS ""

CMD ansible-playbook ${ATLAS_ANSIBLE_PLAYBOOK} ${ATLAS_ANSIBLE_PLAYBOOK_EXTRA_PARAMS}
