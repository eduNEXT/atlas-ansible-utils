FROM docker.io/ubuntu:20.04

RUN apt update && \
  apt upgrade -y && \
  # python 3.8
  apt install -y git python3 python3-pip make
RUN ln -s /usr/bin/python3 /usr/bin/python

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
