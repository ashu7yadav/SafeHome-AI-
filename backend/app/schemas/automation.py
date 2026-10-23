from datetime import datetime
from typing import Optional, Dict, Any
from pydantic import BaseModel, Field, ConfigDict


class AutomationCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=120)
    description: str = Field(..., min_length=2)
    trigger_type: str = Field(..., pattern="^(motion|schedule|geofence|scene)$")
    trigger_configuration: Optional[Dict[str, Any]] = None
    action_configuration: Optional[Dict[str, Any]] = None
    is_enabled: bool = True


class AutomationUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=2, max_length=120)
    description: Optional[str] = None
    trigger_type: Optional[str] = None
    trigger_configuration: Optional[Dict[str, Any]] = None
    action_configuration: Optional[Dict[str, Any]] = None
    is_enabled: Optional[bool] = None


class AutomationResponse(BaseModel):
    id: str
    household_id: str
    name: str
    description: str
    trigger_type: str
    trigger_configuration: Dict[str, Any]
    action_configuration: Dict[str, Any]
    is_enabled: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class AutomationTestResult(BaseModel):
    automation_id: str
    name: str
    status: str
    simulated_actions: list
    message: str
