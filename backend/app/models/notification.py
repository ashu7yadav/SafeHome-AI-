import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Boolean, DateTime, Text, ForeignKey
from app.core.database import Base


def generate_uuid():
    return str(uuid.uuid4())


class Notification(Base):
    __tablename__ = "notifications"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    household_id = Column(String(36), nullable=False, index=True)
    title = Column(String(200), nullable=False)
    message = Column(Text, nullable=False)
    notification_type = Column(String(64), nullable=False, default="security_alert")
    # "security_alert", "routine", "device_status", "system"
    is_read = Column(Boolean, default=False, nullable=False, index=True)
    related_event_id = Column(String(36), ForeignKey("security_events.id", ondelete="SET NULL"), nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False, index=True)
