import os
from proxmoxer import ProxmoxAPI
PROX_HOST = os.getenv("PROXMOX_API_HOST")
PROX_USER = os.getenv("PROXMOX_API_USER")
PROX_PASS = os.getenv("PROXMOX_API_PASSWORD")
proxmox = ProxmoxAPI(PROX_HOST, user=PROX_USER, password=PROX_PASS, verify_ssl=False)

def clone_template(template_vmid: int, new_vmid: int, name: str, cores: int=2, memory:int=2048):
    node = PROX_HOST
    proxmox.nodes(node).qemu(template_vmid).clone.create(newid=new_vmid, name=name, full=1, target=node)
    proxmox.nodes(node).qemu(new_vmid).config.post(cores=cores, memory=memory)
    return new_vmid
