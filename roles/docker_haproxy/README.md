Ansible Role: Docker HAProxy
============================

This role runs HAProxy as an entry point for web traffic to an RKE2 cluster and,
optionally, the Kubernetes API. It provides a shared address for cluster ingress
and API access, along with optional Prometheus metrics.

Role Variables
--------------

Available variables are listed below. Default values are defined in
`defaults/main.yml`.

- `DOCKER_HAPROXY_IMAGE`: Docker image used to run HAProxy.
- `DOCKER_HAPROXY_BIND_ADDRESS`: Address for the built-in HTTP and HTTPS entry
  points.
- `DOCKER_HAPROXY_BACKENDS`: Addresses of the RKE2 worker nodes that house the
  ingress controller pods.
- `DOCKER_HAPROXY_HTTP_PORT`: HTTP port on ingress nodes exposed by the ingress
  controller in Node Port mode.
- `DOCKER_HAPROXY_HTTPS_PORT`: HTTPS port on ingress nodes exposed by the
  ingress controller in Node Port mode.
- `DOCKER_HAPROXY_K8S_API_HOSTNAME`: Hostname clients use to access the
  Kubernetes API.
- `DOCKER_HAPROXY_K8S_API_BACKENDS`: Addresses of control-plane nodes serving
  the Kubernetes API.
- `DOCKER_HAPROXY_K8S_API_PORT`: Kubernetes API port on control-plane nodes.
- `DOCKER_HAPROXY_K8S_API_ALLOWED_CIDRS`: Client address ranges allowed to
  access the Kubernetes API; an empty list denies access.
- `DOCKER_HAPROXY_STATS_ENABLED`: Enables Prometheus metrics at
  `http://<haproxy-host>:9100/metrics`. The endpoint listens on all host
  interfaces; firewall rules should restrict access to trusted scrapers.
- `DOCKER_HAPROXY_ADDITIONAL_SECTIONS`: Optional raw HAProxy sections for
  uncommon services or routing needs.

Dependencies
------------

`docker_install` (included as a role dependency).

Example Playbook
----------------

    - name: Deploy HAProxy for an RKE2 cluster
      hosts: haproxy_servers
      gather_facts: true
      become: false
      roles:
        - role: docker_haproxy

Example inventory variables:

    DOCKER_HAPROXY_BACKENDS: [10.0.0.11, 10.0.0.12]
    DOCKER_HAPROXY_K8S_API_HOSTNAME: api.example.com
    DOCKER_HAPROXY_K8S_API_BACKENDS: [10.0.0.10]
    DOCKER_HAPROXY_K8S_API_ALLOWED_CIDRS: [198.51.100.24/32]
    DOCKER_HAPROXY_STATS_ENABLED: true

The DNS record for `api.example.com` should resolve to the HAProxy host, and the
hostname should be included in the API server certificate. The CIDR list should
contain client source addresses as observed by HAProxy.
