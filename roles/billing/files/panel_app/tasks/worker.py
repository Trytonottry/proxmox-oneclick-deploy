from celery import Celery
import os
from panel_app.proxmox_helper import proxmox, clone_template
from panel_app.db import SessionLocal
from panel_app.models import VMRecord, Invoice
celery = Celery("panel_tasks", broker=os.getenv("REDIS_URL", "redis://redis:6379/0"))

@celery.task(bind=True)
def create_vm_task(self, payload):
    resources = proxmox.cluster.resources.get(type='vm')
    existing = [int(r['vmid']) for r in resources if 'vmid' in r]
    new_vmid = max(existing) + 1 if existing else 100
    try:
        clone_template(payload["template_vmid"], new_vmid, payload["name"], cores=payload.get("cores",2), memory=payload.get("memory",2048))
        db = SessionLocal()
        try:
            vm = VMRecord(vmid=new_vmid, name=payload["name"], status="running")
            db.add(vm); db.commit()
            if payload.get("invoice_id"):
                inv = db.query(Invoice).filter_by(invoice_id=payload["invoice_id"]).first()
                if inv:
                    inv.vm_id = vm.id; db.add(inv); db.commit()
        finally:
            db.close()
        return {"status":"created","vmid": new_vmid}
    except Exception as e:
        db = SessionLocal()
        try:
            if payload.get("invoice_id"):
                inv = db.query(Invoice).filter_by(invoice_id=payload["invoice_id"]).first()
                if inv:
                    inv.status = "failed"; db.add(inv); db.commit()
        finally:
            db.close()
        raise e
