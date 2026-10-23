from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.user import User
from app.models.device import Device
from app.models.security_event import SecurityEvent
from app.models.notification import Notification
from app.api.deps import get_current_user

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])


@router.get("/summary")
def get_dashboard_summary(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    household_id = current_user.household_id

    # Devices total and status
    devices = db.query(Device).filter(Device.household_id == household_id).all()
    total_devices = len(devices)
    online_devices = sum(1 for d in devices if d.is_online)
    offline_devices = total_devices - online_devices

    # Category counts
    cameras = [d for d in devices if d.device_type == "security_camera"]
    cameras_total = len(cameras)
    cameras_online = sum(1 for d in cameras if d.is_online)

    lights = [d for d in devices if d.device_type == "smart_light"]
    lights_total = len(lights)
    lights_enabled = sum(1 for d in lights if d.is_enabled)

    speakers = [d for d in devices if d.device_type == "speaker"]
    wifi_devices = [d for d in devices if d.device_type == "wifi_device"]
    assistants = [d for d in devices if d.device_type == "smart_assistant"]

    # Security & alerts
    active_alerts = db.query(SecurityEvent).filter(
        SecurityEvent.household_id == household_id,
        SecurityEvent.is_acknowledged == False,
        SecurityEvent.severity.in_(["warning", "critical"])
    ).count()

    unread_notifications = db.query(Notification).filter(
        Notification.household_id == household_id,
        Notification.is_read == False
    ).count()

    recent_events = db.query(SecurityEvent).filter(
        SecurityEvent.household_id == household_id
    ).order_by(SecurityEvent.created_at.desc()).limit(5).all()

    return {
        "devices": {
            "total": total_devices,
            "online": online_devices,
            "offline": offline_devices,
            "categories": {
                "cctv": {"count": cameras_total, "online": cameras_online},
                "lighting": {"count": lights_total, "enabled": lights_enabled},
                "speaker": {"count": len(speakers), "online": sum(1 for s in speakers if s.is_online)},
                "wifi": {"count": len(wifi_devices), "online": sum(1 for w in wifi_devices if w.is_online)},
                "assistant": {"count": len(assistants), "online": sum(1 for a in assistants if a.is_online)}
            }
        },
        "security": {
            "status": "All systems checked" if active_alerts == 0 else "Alert needs review",
            "active_alerts": active_alerts,
            "cameras_online": cameras_online,
            "cameras_total": cameras_total
        },
        "lighting": {
            "total": lights_total,
            "enabled": lights_enabled
        },
        "notifications": {
            "unread": unread_notifications
        },
        "recent_events": [
            {
                "id": e.id,
                "title": e.title,
                "description": e.description,
                "severity": e.severity,
                "event_type": e.event_type,
                "is_acknowledged": e.is_acknowledged,
                "created_at": e.created_at
            }
            for e in recent_events
        ],
        "demo_mode": True,
        "household_id": household_id
    }
