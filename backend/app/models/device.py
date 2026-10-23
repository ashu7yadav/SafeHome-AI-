import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Boolean, DateTime, Text
from app.core.database import Base


def generate_uuid():
    return str(uuid.uuid4())


class Device(Base):
    __tablename__ = "devices"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    household_id = Column(String(36), nullable=False, index=True)
    name = Column(String(120), nullable=False)
    device_type = Column(String(64), nullable=False, index=True)
    # Types: "security_camera", "smart_light", "thermostat", "door_lock",
    #        "smart_blinds", "smart_vacuum", "speaker", "wifi_device", "smart_assistant"
    room = Column(String(64), nullable=False, default="Living Room")
    status = Column(String(64), nullable=False, default="online")
    is_online = Column(Boolean, default=True, nullable=False)
    is_enabled = Column(Boolean, default=True, nullable=False)
    configuration_json = Column(Text, default="{}", nullable=False)
    last_seen = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = Column(
        DateTime, 
        default=lambda: datetime.now(timezone.utc), 
        onupdate=lambda: datetime.now(timezone.utc), 
        nullable=False
    )
