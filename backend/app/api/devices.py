from typing import List, Optional
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.user import User
from app.schemas.device import (
    DeviceCreate, 
    DeviceUpdate, 
    DevicePowerUpdate, 
    BrightnessUpdate, 
    TemperatureUpdate, 
    BlindsUpdate, 
    VacuumUpdate, 
    DeviceResponse
)
from app.services.device_service import DeviceService
from app.api.deps import get_current_user

router = APIRouter(prefix="/devices", tags=["Smart Devices"])


@router.get("", response_model=List[DeviceResponse])
def get_devices(
    device_type: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return DeviceService.get_devices(db, current_user.household_id, device_type)


@router.post("", response_model=DeviceResponse, status_code=status.HTTP_201_CREATED)
def create_device(
    device_in: DeviceCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return DeviceService.create_device(db, current_user.household_id, device_in)


@router.get("/{device_id}", response_model=DeviceResponse)
def get_device(
    device_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return DeviceService.get_device(db, current_user.household_id, device_id)


@router.patch("/{device_id}", response_model=DeviceResponse)
def update_device(
    device_id: str,
    device_in: DeviceUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return DeviceService.update_device(db, current_user.household_id, device_id, device_in)


@router.delete("/{device_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_device(
    device_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    DeviceService.delete_device(db, current_user.household_id, device_id)


@router.patch("/{device_id}/power", response_model=DeviceResponse)
def set_device_power(
    device_id: str,
    payload: DevicePowerUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return DeviceService.set_power(db, current_user.household_id, device_id, payload)


@router.patch("/{device_id}/brightness", response_model=DeviceResponse)
def set_light_brightness(
    device_id: str,
    payload: BrightnessUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return DeviceService.set_brightness(db, current_user.household_id, device_id, payload)


@router.patch("/{device_id}/temperature", response_model=DeviceResponse)
def set_thermostat_temperature(
    device_id: str,
    payload: TemperatureUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return DeviceService.set_temperature(db, current_user.household_id, device_id, payload)


@router.patch("/{device_id}/blinds", response_model=DeviceResponse)
def set_blinds_percentage(
    device_id: str,
    payload: BlindsUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return DeviceService.set_blinds(db, current_user.household_id, device_id, payload)


@router.patch("/{device_id}/vacuum", response_model=DeviceResponse)
def set_vacuum_state(
    device_id: str,
    payload: VacuumUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return DeviceService.set_vacuum(db, current_user.household_id, device_id, payload)
