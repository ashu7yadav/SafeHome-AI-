import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, DateTime
from app.core.database import Base


def generate_uuid():
    return str(uuid.uuid4())


class Visitor(Base):
    __tablename__ = "visitors"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    household_id = Column(String(36), nullable=False, index=True)
    visitor_name = Column(String(120), nullable=False)
    contact_information = Column(String(200), nullable=True)
    purpose = Column(String(200), nullable=False)  # "Package Delivery", "Home Maintenance", "Family Visit"
    access_status = Column(String(32), default="approved", nullable=False)  # "pending", "approved", "revoked", "expired"
    valid_from = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    valid_until = Column(DateTime, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    approved_by = Column(String(120), nullable=True)
