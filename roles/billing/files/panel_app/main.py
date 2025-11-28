from fastapi import FastAPI, HTTPException, BackgroundTasks, Request, Header
from pydantic import BaseModel
import os, logging, hmac, hashlib
from .crypto import cryptocloud_create_invoice
from .db import SessionLocal, engine
from .models import Base, Invoice, PaymentEvent
from datetime import datetime
from tasks.worker import create_vm_task

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Panel Skeleton")
logger = logging.getLogger("uvicorn.error")
CRYPTOCLOUD_SECRET = os.getenv("CRYPTOCLOUD_SECRET", "")

class CreateInvoiceReq(BaseModel):
    amount: float
    currency: str = "USD"
    description: str = ""

@app.post("/api/v1/create-invoice")
def create_invoice(req: CreateInvoiceReq):
    try:
        invoice = cryptocloud_create_invoice(amount=req.amount, currency=req.currency, description=req.description)
        # store invoice in DB - minimal flow
        db = SessionLocal()
        inv = Invoice(invoice_id=str(invoice.get('invoice_id', invoice.get('id','unknown'))),
                      amount=req.amount, currency=req.currency, description=req.description, status='created', metadata={})
        db.add(inv); db.commit(); db.close()
        return invoice
    except Exception as e:
        logger.exception("invoice error")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/v1/webhook/cryptocloud")
async def cryptocloud_webhook(request: Request, x_signature: str = Header(None)):
    body = await request.body()
    if CRYPTOCLOUD_SECRET:
        mac = hmac.new(CRYPTOCLOUD_SECRET.encode(), body, hashlib.sha256).hexdigest()
        if not x_signature or not hmac.compare_digest(mac, x_signature):
            raise HTTPException(status_code=400, detail="invalid signature")
    payload = await request.json()
    db = SessionLocal()
    try:
        evt = PaymentEvent(invoice_id=payload.get("invoice_id",""), event_type=payload.get("status","webhook_received"), payload=payload)
        db.add(evt); db.commit()
        # handle paid
        if payload.get("status") in ("paid", "confirmed"):
            inv = db.query(Invoice).filter_by(invoice_id=payload.get("invoice_id")).first()
            if inv:
                inv.status = "paid"; inv.paid_at = datetime.utcnow(); db.add(inv); db.commit()
                # if metadata contains vm_request, trigger create_vm_task
                meta = inv.metadata or {}
                if meta.get("auto_create_vm"):
                    create_vm_task.delay(meta["vm_request"])
    finally:
        db.close()
    return {"status":"ok"}
