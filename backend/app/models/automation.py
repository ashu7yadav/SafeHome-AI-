import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Boolean, DateTime, Text
from app.core.database import Base


def generate_uuid():
    return str(uuid.uuid4())


class Automation(Base):
    __tablename__ = "automations"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    household_id = Column(String(36), nullable=False, index=True)
    name = Column(String(120), nullable=False)
    description = Column(Text, nullable=False)
    trigger_type = Column(String(64), nullable=False)  # "motion", "schedule", "geofence", "scene"
    trigger_configuration = Column(Text, default="{}", nullable=False)
    action_configuration = Column(Text, default="{}", nullable=False)
    is_enabled = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = Column(
        DateTime, 
        default=lambda: datetime.now(timezone.utc), 
        onupdate=lambda: datetime.now(timezone.utc), 
        nullable=False
    )
