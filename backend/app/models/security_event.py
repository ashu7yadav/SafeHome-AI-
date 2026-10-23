import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Boolean, DateTime, Text, ForeignKey
from app.core.database import Base


def generate_uuid():
    return str(uuid.uuid4())


class SecurityEvent(Base):
    __tablename__ = "security_events"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    household_id = Column(String(36), nullable=False, index=True)
    device_id = Column(String(36), ForeignKey("devices.id", ondelete="SET NULL"), nullable=True)
    event_type = Column(String(64), nullable=False, index=True)
    # Types: "motion_detection", "door_access", "device_disconnection", "unusual_activity", "system_status"
    severity = Column(String(32), nullable=False, default="informational")
    # Severity: "informational", "warning", "critical"
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=False)
    source = Column(String(64), nullable=False, default="simulated")
    # Source: "simulated", "smart_doorbell", "security_camera", "door_lock", "system"
    is_acknowledged = Column(Boolean, default=False, nullable=False, index=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False, index=True)
    acknowledged_at = Column(DateTime, nullable=True)
    acknowledged_by = Column(String(120), nullable=True)
