from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict


class SecurityEventCreate(BaseModel):
    device_id: Optional[str] = None
    event_type: str = Field(..., max_length=64)
    severity: str = Field("informational", pattern="^(informational|warning|critical)$")
    title: str = Field(..., min_length=1, max_length=200)
    description: str = Field(..., min_length=1)
    source: str = Field("simulated", max_length=64)


class SecurityEventDemo(BaseModel):
    event_type: Optional[str] = "motion_detection"
    camera_id: Optional[str] = None
    location: Optional[str] = "Front entrance"


class SecurityEventAcknowledge(BaseModel):
    notes: Optional[str] = None


class SecurityEventResponse(BaseModel):
    id: str
    household_id: str
    device_id: Optional[str] = None
    event_type: str
    severity: str
    title: str
    description: str
    source: str
    is_acknowledged: bool
    created_at: datetime
    acknowledged_at: Optional[datetime] = None
    acknowledged_by: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)
