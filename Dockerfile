FROM python:3.12-slim-bookworm AS minimal
ARG DEBIAN_FRONTEND=noninteractive

RUN --mount=type=cache,target=/var/cache/apt,sharing=locked \
    --mount=type=cache,target=/var/lib/apt,sharing=locked \
    <<EOCMD
    apt update
    apt install -y \
        build-essential \
        git \
    ;
EOCMD

FROM minimal AS dependencies
WORKDIR /deps
COPY --from=ghcr.io/astral-sh/uv:0.10.2 /uv /usr/local/bin
ENV VIRTUAL_ENV=/opt/venv
ENV UV_LINK_MODE=copy
ENV UV_COMPILE_BYTECODE=1
RUN uv venv ${VIRTUAL_ENV}

RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --active --frozen --no-install-project --no-dev --no-editable

FROM minimal AS final
COPY --from=dependencies /opt/venv /opt/venv

ENV VIRTUAL_ENV=/opt/venv
ENV PATH="/opt/venv/bin:${PATH}"

WORKDIR /runner

COPY  ./hosts.ini /etc/ansible/

RUN <<EOCMD
    set -eux; \
    groupadd --system --gid 1000 runner; \
    useradd --system --gid runner --uid 1000 --home-dir /runner runner; \
    chown -R 1000:1000 /runner;
EOCMD

COPY . .

USER 1000:1000

# For now, we prefer skipping the host key checking
ENV ANSIBLE_HOST_KEY_CHECKING="no"
ENV ATLAS_ANSIBLE_PLAYBOOK="test_os_info.yml"
ENV ATLAS_ANSIBLE_PLAYBOOK_EXTRA_PARAMS=""
ENV ANSIBLE_INVENTORY="/etc/ansible/hosts.ini"

ENTRYPOINT [ "/runner/entrypoint.sh"]
