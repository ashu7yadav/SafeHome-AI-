from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.user import User
from app.models.device import Device
from app.services.device_service import DeviceService
from app.api.deps import get_current_user

router = APIRouter(prefix="/cameras", tags=["Security Cameras"])


@router.get("")
def list_cameras(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    cameras = db.query(Device).filter(
        Device.household_id == current_user.household_id,
        Device.device_type == "security_camera"
    ).order_by(Device.created_at.asc()).all()

    results = []
    for cam in cameras:
        config = DeviceService._parse_config(cam)
        results.append({
            "id": cam.id,
            "name": cam.name,
            "location": cam.room,
            "is_online": cam.is_online,
            "status": cam.status,
            "is_simulated": True,
            "stream_resolution": config.get("stream_resolution", "FHD 1080p"),
            "image_url": config.get("image_url", ""),
            "capabilities": ["live_stream", "two_way_audio", "night_vision", "motion_tripwire"],
            "last_seen": cam.last_seen
        })
    return results


@router.get("/{camera_id}")
def get_camera(
    camera_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    cam = db.query(Device).filter(
        Device.id == camera_id,
        Device.household_id == current_user.household_id,
        Device.device_type == "security_camera"
    ).first()
    if not cam:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Camera not found")

    config = DeviceService._parse_config(cam)
    return {
        "id": cam.id,
        "name": cam.name,
        "location": cam.room,
        "is_online": cam.is_online,
        "status": cam.status,
        "is_simulated": True,
        "stream_resolution": config.get("stream_resolution", "FHD 1080p"),
        "image_url": config.get("image_url", ""),
        "capabilities": ["live_stream", "two_way_audio", "night_vision", "motion_tripwire"],
        "last_seen": cam.last_seen
    }


@router.get("/{camera_id}/status")
def get_camera_status(
    camera_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    cam = db.query(Device).filter(
        Device.id == camera_id,
        Device.household_id == current_user.household_id,
        Device.device_type == "security_camera"
    ).first()
    if not cam:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Camera not found")

    return {
        "camera_id": cam.id,
        "name": cam.name,
        "is_online": cam.is_online,
        "connection_quality": "excellent" if cam.is_online else "disconnected",
        "fps": 30 if cam.is_online else 0,
        "bitrate_mbps": 4.2 if cam.is_online else 0.0,
        "is_simulated": True
    }
