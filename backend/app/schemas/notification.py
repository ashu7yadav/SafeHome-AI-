from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict


class NotificationCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    message: str = Field(..., min_length=1)
    notification_type: str = "security_alert"
    related_event_id: Optional[str] = None


class NotificationResponse(BaseModel):
    id: str
    household_id: str
    title: str
    message: str
    notification_type: str
    is_read: bool
    related_event_id: Optional[str] = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class UnreadCountResponse(BaseModel):
    unread_count: int
