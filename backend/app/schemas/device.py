from datetime import datetime
from typing import Optional, Dict, Any
from pydantic import BaseModel, Field, ConfigDict


class DeviceBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=120)
    device_type: str = Field(..., min_length=1, max_length=64)
    room: str = Field("Living Room", max_length=64)
    is_online: bool = True
    is_enabled: bool = True
    configuration: Optional[Dict[str, Any]] = None


class DeviceCreate(DeviceBase):
    pass


class DeviceUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=120)
    room: Optional[str] = Field(None, max_length=64)
    is_online: Optional[bool] = None
    is_enabled: Optional[bool] = None
    status: Optional[str] = None
    configuration: Optional[Dict[str, Any]] = None


class DevicePowerUpdate(BaseModel):
    is_enabled: bool


class BrightnessUpdate(BaseModel):
    brightness: int = Field(..., ge=0, le=100)


class TemperatureUpdate(BaseModel):
    temperature: float = Field(..., ge=10, le=95)
    mode: Optional[str] = "heat"


class BlindsUpdate(BaseModel):
    opening_percentage: int = Field(..., ge=0, le=100)


class VacuumUpdate(BaseModel):
    is_running: bool
    mode: Optional[str] = "auto"


class DeviceResponse(BaseModel):
    id: str
    household_id: str
    name: str
    device_type: str
    room: str
    status: str
    is_online: bool
    is_enabled: bool
    configuration: Dict[str, Any]
    last_seen: datetime
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
