# proxmox-oneclick
![Ansible](https://img.shields.io/badge/ansible-automation-red?logo=ansible)
![Proxmox](https://img.shields.io/badge/proxmox-cluster-orange?logo=proxmox)
![ZFS](https://img.shields.io/badge/storage-ZFS-blue?logo=ubuntu)
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
![FastAPI](https://img.shields.io/badge/backend-FastAPI-009688?logo=fastapi)
![Traefik](https://img.shields.io/badge/reverse_proxy-Traefik-2F9EBE?logo=traefik)
![Docker](https://img.shields.io/badge/docker-containers-2496ED?logo=docker)
![Redis](https://img.shields.io/badge/cache-redis-DC382D?logo=redis)
![Postgres](https://img.shields.io/badge/database-postgres-4169E1?logo=postgresql)
![CryptoCloud](https://img.shields.io/badge/payments-CryptoCloud-purple?logo=bitcoin)
![Minecraft](https://img.shields.io/badge/game-Minecraft-62B47A?logo=minecraft)
![Factorio](https://img.shields.io/badge/game-Factorio-E78300?logo=factorio)
![VDS](https://img.shields.io/badge/VDS-automation-important)
![Prometheus](https://img.shields.io/badge/metrics-Prometheus-orange?logo=prometheus)
![Grafana](https://img.shields.io/badge/dashboards-Grafana-F46800?logo=grafana)
![API](https://img.shields.io/badge/API-json--rpc-yellow)
![Webhooks](https://img.shields.io/badge/webhooks-automated-blueviolet)

One-click skeleton for deploying a Proxmox cluster with ZFS, templates, billing panel (FastAPI + CryptoCloud), monitoring, Traefik and game servers.

## What is included
- Ansible playbooks to bootstrap Proxmox cluster, create ZFS pool, upload cloud templates.
- Roles for billing (FastAPI + Celery + Redis + Postgres), monitoring (Prometheus/Grafana), Traefik, games provisioning (Minecraft, Factorio).
- Panel skeleton with CryptoCloud integration (invoice creation + webhook handling), Celery worker to create VMs via Proxmox API.
- ZFS replication and restore-test playbooks.
- CI workflow for building and publishing panel image.

## Quick start
1. Clone repository to your machine.
2. Edit `inventory/hosts.ini` and `group_vars/all.yml` to fit your environment.
3. Put secrets into ansible-vault:
   ```bash
   ansible-vault create group_vars/vault.yml
   ```
   Store: PROXMOX_API_PASSWORD, CRYPTOCLOUD_API_KEY, CRYPTOCLOUD_SECRET, DB passwords, DNS provider tokens.
4. Install requirements:
   ```bash
   ansible-galaxy collection install -r requirements.yml
   ```
5. Run one-click:
   ```bash
   ansible-playbook -i inventory/hosts.ini playbooks/proxmox-setup.yml --ask-vault-pass
   ```

## Security & production checklist
- Use non-root Proxmox API user instead of root@pam.
- Use DNS ACME for Traefik and keep DNS provider credentials in vault.
- Ensure SSH keys and vault secrets are protected.
- Test ZFS restore weekly, monitor replication metrics.
- Use CryptoCloud sandbox keys for staging tests before going live.

## Notes
- Factorio requires licensed download; provide archive path if you want full automation.
- This skeleton aims to be a practical starting point — adapt playbooks/roles to your exact infra and policies.

