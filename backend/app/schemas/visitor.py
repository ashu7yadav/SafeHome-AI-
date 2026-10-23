from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict


class VisitorCreate(BaseModel):
    visitor_name: str = Field(..., min_length=2, max_length=120)
    contact_information: Optional[str] = Field(None, max_length=200)
    purpose: str = Field(..., min_length=2, max_length=200)
    valid_from: Optional[datetime] = None
    valid_until: datetime


class VisitorUpdate(BaseModel):
    visitor_name: Optional[str] = Field(None, min_length=2, max_length=120)
    contact_information: Optional[str] = None
    purpose: Optional[str] = None
    access_status: Optional[str] = None
    valid_until: Optional[datetime] = None


class VisitorResponse(BaseModel):
    id: str
    household_id: str
    visitor_name: str
    contact_information: Optional[str] = None
    purpose: str
    access_status: str
    valid_from: datetime
    valid_until: datetime
    created_at: datetime
    approved_by: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)
