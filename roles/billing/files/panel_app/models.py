from sqlalchemy import Column, Integer, String, DateTime, Float, JSON, ForeignKey, func
from sqlalchemy.orm import declarative_base, relationship
Base = declarative_base()
class VMRecord(Base):
    __tablename__ = "vm"
    id = Column(Integer, primary_key=True, index=True)
    vmid = Column(Integer, unique=True, nullable=False, index=True)
    name = Column(String, nullable=False)
    owner_id = Column(Integer, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    status = Column(String, default="provisioning")
class Invoice(Base):
    __tablename__ = "invoices"
    id = Column(Integer, primary_key=True, index=True)
    invoice_id = Column(String, unique=True, nullable=False)
    amount = Column(Float, nullable=False)
    currency = Column(String, nullable=False)
    description = Column(String, nullable=True)
    status = Column(String, nullable=False, default="created")
    metadata = Column(JSON, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    paid_at = Column(DateTime(timezone=True), nullable=True)
    vm_id = Column(Integer, ForeignKey("vm.id"), nullable=True)
    vm = relationship("VMRecord", backref="invoice")
class PaymentEvent(Base):
    __tablename__ = "payment_events"
    id = Column(Integer, primary_key=True, index=True)
    invoice_id = Column(String, nullable=False, index=True)
    event_type = Column(String, nullable=False)
    payload = Column(JSON)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
