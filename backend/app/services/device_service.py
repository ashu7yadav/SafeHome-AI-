import json
from datetime import datetime, timezone
from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.device import Device
from app.schemas.device import (
    DeviceCreate, 
    DeviceUpdate, 
    DevicePowerUpdate, 
    BrightnessUpdate, 
    TemperatureUpdate, 
    BlindsUpdate, 
    VacuumUpdate
)


class DeviceService:
    @staticmethod
    def _parse_config(device: Device) -> Dict[str, Any]:
        try:
            return json.loads(device.configuration_json or "{}")
        except Exception:
            return {}

    @staticmethod
    def _to_response_dict(device: Device) -> dict:
        return {
            "id": device.id,
            "household_id": device.household_id,
            "name": device.name,
            "device_type": device.device_type,
            "room": device.room,
            "status": device.status,
            "is_online": device.is_online,
            "is_enabled": device.is_enabled,
            "configuration": DeviceService._parse_config(device),
            "last_seen": device.last_seen,
            "created_at": device.created_at,
            "updated_at": device.updated_at,
        }

    @staticmethod
    def get_devices(db: Session, household_id: str, device_type: Optional[str] = None) -> List[dict]:
        query = db.query(Device).filter(Device.household_id == household_id)
        if device_type:
            query = query.filter(Device.device_type == device_type)
        devices = query.order_by(Device.created_at.asc()).all()
        return [DeviceService._to_response_dict(d) for d in devices]

    @staticmethod
    def get_device(db: Session, household_id: str, device_id: str) -> dict:
        device = db.query(Device).filter(
            Device.id == device_id, 
            Device.household_id == household_id
        ).first()
        if not device:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Device not found")
        return DeviceService._to_response_dict(device)

    @staticmethod
    def create_device(db: Session, household_id: str, obj_in: DeviceCreate) -> dict:
        config_str = json.dumps(obj_in.configuration or {})
        device = Device(
            household_id=household_id,
            name=obj_in.name,
            device_type=obj_in.device_type,
            room=obj_in.room,
            is_online=obj_in.is_online,
            is_enabled=obj_in.is_enabled,
            status="online" if obj_in.is_online else "offline",
            configuration_json=config_str,
            last_seen=datetime.now(timezone.utc)
        )
        db.add(device)
        db.commit()
        db.refresh(device)
        return DeviceService._to_response_dict(device)

    @staticmethod
    def update_device(db: Session, household_id: str, device_id: str, obj_in: DeviceUpdate) -> dict:
        device = db.query(Device).filter(
            Device.id == device_id, 
            Device.household_id == household_id
        ).first()
        if not device:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Device not found")

        update_data = obj_in.model_dump(exclude_unset=True)
        if "configuration" in update_data:
            current_config = DeviceService._parse_config(device)
            current_config.update(update_data.pop("configuration") or {})
            device.configuration_json = json.dumps(current_config)

        for field, value in update_data.items():
            setattr(device, field, value)

        device.last_seen = datetime.now(timezone.utc)
        db.commit()
        db.refresh(device)
        return DeviceService._to_response_dict(device)

    @staticmethod
    def delete_device(db: Session, household_id: str, device_id: str) -> None:
        device = db.query(Device).filter(
            Device.id == device_id, 
            Device.household_id == household_id
        ).first()
        if not device:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Device not found")
        db.delete(device)
        db.commit()

    @staticmethod
    def set_power(db: Session, household_id: str, device_id: str, obj_in: DevicePowerUpdate) -> dict:
        device = db.query(Device).filter(
            Device.id == device_id, 
            Device.household_id == household_id
        ).first()
        if not device:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Device not found")

        device.is_enabled = obj_in.is_enabled
        device.status = "active" if obj_in.is_enabled else "standby"
        device.last_seen = datetime.now(timezone.utc)
        db.commit()
        db.refresh(device)
        return DeviceService._to_response_dict(device)

    @staticmethod
    def set_brightness(db: Session, household_id: str, device_id: str, obj_in: BrightnessUpdate) -> dict:
        device = db.query(Device).filter(
            Device.id == device_id, 
            Device.household_id == household_id
        ).first()
        if not device:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Device not found")
        if device.device_type != "smart_light":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, 
                detail="Brightness control only applies to smart lights"
            )

        config = DeviceService._parse_config(device)
        config["brightness"] = obj_in.brightness
        device.configuration_json = json.dumps(config)
        device.is_enabled = obj_in.brightness > 0
        device.last_seen = datetime.now(timezone.utc)
        db.commit()
        db.refresh(device)
        return DeviceService._to_response_dict(device)

    @staticmethod
    def set_temperature(db: Session, household_id: str, device_id: str, obj_in: TemperatureUpdate) -> dict:
        device = db.query(Device).filter(
            Device.id == device_id, 
            Device.household_id == household_id
        ).first()
        if not device:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Device not found")
        if device.device_type != "thermostat":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, 
                detail="Temperature control only applies to thermostats"
            )

        config = DeviceService._parse_config(device)
        config["target_temperature"] = obj_in.temperature
        if obj_in.mode:
            config["mode"] = obj_in.mode
        device.configuration_json = json.dumps(config)
        device.last_seen = datetime.now(timezone.utc)
        db.commit()
        db.refresh(device)
        return DeviceService._to_response_dict(device)

    @staticmethod
    def set_blinds(db: Session, household_id: str, device_id: str, obj_in: BlindsUpdate) -> dict:
        device = db.query(Device).filter(
            Device.id == device_id, 
            Device.household_id == household_id
        ).first()
        if not device:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Device not found")
        if device.device_type != "smart_blinds":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, 
                detail="Opening percentage only applies to smart blinds"
            )

        config = DeviceService._parse_config(device)
        config["opening_percentage"] = obj_in.opening_percentage
        device.configuration_json = json.dumps(config)
        device.status = "open" if obj_in.opening_percentage > 0 else "closed"
        device.last_seen = datetime.now(timezone.utc)
        db.commit()
        db.refresh(device)
        return DeviceService._to_response_dict(device)

    @staticmethod
    def set_vacuum(db: Session, household_id: str, device_id: str, obj_in: VacuumUpdate) -> dict:
        device = db.query(Device).filter(
            Device.id == device_id, 
            Device.household_id == household_id
        ).first()
        if not device:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Device not found")
        if device.device_type != "smart_vacuum":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, 
                detail="Vacuum actions only apply to smart vacuums"
            )

        config = DeviceService._parse_config(device)
        config["is_running"] = obj_in.is_running
        if obj_in.mode:
            config["cleaning_mode"] = obj_in.mode
        device.configuration_json = json.dumps(config)
        device.is_enabled = obj_in.is_running
        device.status = "running" if obj_in.is_running else "docked"
        device.last_seen = datetime.now(timezone.utc)
        db.commit()
        db.refresh(device)
        return DeviceService._to_response_dict(device)
