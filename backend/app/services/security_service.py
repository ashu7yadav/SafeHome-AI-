from datetime import datetime, timezone
from typing import List, Optional
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.security_event import SecurityEvent
from app.models.notification import Notification
from app.models.device import Device
from app.schemas.event import SecurityEventCreate, SecurityEventDemo


class SecurityService:
    @staticmethod
    def get_events(
        db: Session,
        household_id: str,
        severity: Optional[str] = None,
        event_type: Optional[str] = None,
        is_acknowledged: Optional[bool] = None,
        skip: int = 0,
        limit: int = 50
    ) -> List[SecurityEvent]:
        query = db.query(SecurityEvent).filter(SecurityEvent.household_id == household_id)
        if severity:
            query = query.filter(SecurityEvent.severity == severity)
        if event_type:
            query = query.filter(SecurityEvent.event_type == event_type)
        if is_acknowledged is not None:
            query = query.filter(SecurityEvent.is_acknowledged == is_acknowledged)
        return query.order_by(SecurityEvent.created_at.desc()).offset(skip).limit(limit).all()

    @staticmethod
    def get_event(db: Session, household_id: str, event_id: str) -> SecurityEvent:
        event = db.query(SecurityEvent).filter(
            SecurityEvent.id == event_id,
            SecurityEvent.household_id == household_id
        ).first()
        if not event:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Event not found")
        return event

    @staticmethod
    def acknowledge_event(db: Session, household_id: str, event_id: str, user_name: str) -> SecurityEvent:
        event = db.query(SecurityEvent).filter(
            SecurityEvent.id == event_id,
            SecurityEvent.household_id == household_id
        ).first()
        if not event:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Event not found")

        event.is_acknowledged = True
        event.acknowledged_at = datetime.now(timezone.utc)
        event.acknowledged_by = user_name
        db.commit()
        db.refresh(event)
        return event

    @staticmethod
    def acknowledge_all_events(db: Session, household_id: str, user_name: str) -> int:
        now = datetime.now(timezone.utc)
        count = db.query(SecurityEvent).filter(
            SecurityEvent.household_id == household_id,
            SecurityEvent.is_acknowledged == False
        ).update({
            SecurityEvent.is_acknowledged: True,
            SecurityEvent.acknowledged_at: now,
            SecurityEvent.acknowledged_by: user_name
        })
        db.commit()
        return count

    @staticmethod
    def create_demo_event(db: Session, household_id: str, payload: SecurityEventDemo) -> SecurityEvent:
        # Find camera or doorbell device
        device = None
        if payload.camera_id:
            device = db.query(Device).filter(
                Device.id == payload.camera_id,
                Device.household_id == household_id
            ).first()
        if not device:
            device = db.query(Device).filter(
                Device.household_id == household_id,
                Device.device_type == "security_camera"
            ).first()

        loc = payload.location or (device.room if device else "Front entrance")
        title = "Demo: Person detected at " + loc
        desc = "Simulated security detection generated for testing SafeHome AI response workflows."

        event = SecurityEvent(
            household_id=household_id,
            device_id=device.id if device else None,
            event_type=payload.event_type or "motion_detection",
            severity="warning",
            title=title,
            description=desc,
            source="simulated",
            is_acknowledged=False,
            created_at=datetime.now(timezone.utc)
        )
        db.add(event)
        db.commit()
        db.refresh(event)

        # Also create a corresponding notification
        notification = Notification(
            household_id=household_id,
            title=title,
            message=desc,
            notification_type="security_alert",
            is_read=False,
            related_event_id=event.id,
            created_at=datetime.now(timezone.utc)
        )
        db.add(notification)
        db.commit()

        return event

    @staticmethod
    def get_security_status(db: Session, household_id: str) -> dict:
        unacknowledged_alerts = db.query(SecurityEvent).filter(
            SecurityEvent.household_id == household_id,
            SecurityEvent.is_acknowledged == False,
            SecurityEvent.severity.in_(["warning", "critical"])
        ).count()

        cameras_total = db.query(Device).filter(
            Device.household_id == household_id,
            Device.device_type == "security_camera"
        ).count()

        cameras_online = db.query(Device).filter(
            Device.household_id == household_id,
            Device.device_type == "security_camera",
            Device.is_online == True
        ).count()

        latest_event = db.query(SecurityEvent).filter(
            SecurityEvent.household_id == household_id
        ).order_by(SecurityEvent.created_at.desc()).first()

        status_text = "All systems checked" if unacknowledged_alerts == 0 else "Security alert pending review"

        return {
            "status": status_text,
            "is_secure": unacknowledged_alerts == 0,
            "active_alerts_count": unacknowledged_alerts,
            "cameras_online": cameras_online,
            "cameras_total": cameras_total,
            "latest_event": latest_event,
            "demo_mode": True
        }
