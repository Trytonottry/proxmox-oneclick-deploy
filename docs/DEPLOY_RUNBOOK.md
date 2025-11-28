# Deploy Runbook (short)

1. Ensure repo is up-to-date on deploy host:
   ```
   ssh deploy@DEPLOY_HOST 'cd ~/deploy/proxmox-oneclick && git pull'
   ```

2. Put secrets in ansible-vault on deploy host:
   ```
   ansible-vault edit group_vars/vault.yml
   ```

3. Run full setup:
   ```
   ansible-playbook -i inventory/hosts.ini playbooks/proxmox-setup.yml --ask-vault-pass
   ```

4. To deploy new panel image (after CI pushed to Docker Hub):
   ```
   ssh deploy@DEPLOY_HOST 'cd ~/deploy/proxmox-oneclick && ansible-playbook -i inventory/hosts.ini playbooks/deploy-services.yml --ask-vault-pass'
   ```

5. Emergency rollback:
   - Restore VM from ZFS snapshot using `playbooks/zfs-restore-test.yml` instructions.
   - Or revert docker-compose image to previous tag in billing VM and restart.
