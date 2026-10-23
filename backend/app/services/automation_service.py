import json
from datetime import datetime, timezone
from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.automation import Automation
from app.models.security_event import SecurityEvent
from app.models.notification import Notification
from app.schemas.automation import AutomationCreate, AutomationUpdate, AutomationTestResult


class AutomationService:
    @staticmethod
    def _parse_json(text: str) -> Dict[str, Any]:
        try:
            return json.loads(text or "{}")
        except Exception:
            return {}

    @staticmethod
    def _to_response_dict(automation: Automation) -> dict:
        return {
            "id": automation.id,
            "household_id": automation.household_id,
            "name": automation.name,
            "description": automation.description,
            "trigger_type": automation.trigger_type,
            "trigger_configuration": AutomationService._parse_json(automation.trigger_configuration),
            "action_configuration": AutomationService._parse_json(automation.action_configuration),
            "is_enabled": automation.is_enabled,
            "created_at": automation.created_at,
            "updated_at": automation.updated_at,
        }

    @staticmethod
    def get_automations(db: Session, household_id: str) -> List[dict]:
        items = db.query(Automation).filter(
            Automation.household_id == household_id
        ).order_by(Automation.created_at.asc()).all()
        return [AutomationService._to_response_dict(a) for a in items]

    @staticmethod
    def get_automation(db: Session, household_id: str, automation_id: str) -> dict:
        automation = db.query(Automation).filter(
            Automation.id == automation_id,
            Automation.household_id == household_id
        ).first()
        if not automation:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Automation not found")
        return AutomationService._to_response_dict(automation)

    @staticmethod
    def create_automation(db: Session, household_id: str, obj_in: AutomationCreate) -> dict:
        automation = Automation(
            household_id=household_id,
            name=obj_in.name,
            description=obj_in.description,
            trigger_type=obj_in.trigger_type,
            trigger_configuration=json.dumps(obj_in.trigger_configuration or {}),
            action_configuration=json.dumps(obj_in.action_configuration or {}),
            is_enabled=obj_in.is_enabled,
            created_at=datetime.now(timezone.utc)
        )
        db.add(automation)
        db.commit()
        db.refresh(automation)
        return AutomationService._to_response_dict(automation)

    @staticmethod
    def update_automation(db: Session, household_id: str, automation_id: str, obj_in: AutomationUpdate) -> dict:
        automation = db.query(Automation).filter(
            Automation.id == automation_id,
            Automation.household_id == household_id
        ).first()
        if not automation:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Automation not found")

        update_data = obj_in.model_dump(exclude_unset=True)
        if "trigger_configuration" in update_data:
            automation.trigger_configuration = json.dumps(update_data.pop("trigger_configuration"))
        if "action_configuration" in update_data:
            automation.action_configuration = json.dumps(update_data.pop("action_configuration"))

        for field, value in update_data.items():
            setattr(automation, field, value)

        db.commit()
        db.refresh(automation)
        return AutomationService._to_response_dict(automation)

    @staticmethod
    def toggle_automation(db: Session, household_id: str, automation_id: str) -> dict:
        automation = db.query(Automation).filter(
            Automation.id == automation_id,
            Automation.household_id == household_id
        ).first()
        if not automation:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Automation not found")

        automation.is_enabled = not automation.is_enabled
        db.commit()
        db.refresh(automation)
        return AutomationService._to_response_dict(automation)

    @staticmethod
    def delete_automation(db: Session, household_id: str, automation_id: str) -> None:
        automation = db.query(Automation).filter(
            Automation.id == automation_id,
            Automation.household_id == household_id
        ).first()
        if not automation:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Automation not found")
        db.delete(automation)
        db.commit()

    @staticmethod
    def test_automation(db: Session, household_id: str, automation_id: str) -> AutomationTestResult:
        automation = db.query(Automation).filter(
            Automation.id == automation_id,
            Automation.household_id == household_id
        ).first()
        if not automation:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Automation not found")

        actions = AutomationService._parse_json(automation.action_configuration)
        simulated_list = []

        # Safe simulation of automation actions
        if "dim_lights" in actions:
            simulated_list.append(f"Simulated: Dimmed pantry light to {actions['dim_lights']}%")
        if "shut_blinds" in actions:
            simulated_list.append("Simulated: Closed living room blinds")
        if "lock_doors" in actions:
            simulated_list.append("Simulated: Locked front entrance deadbolt")
        if "arm_cameras" in actions:
            simulated_list.append("Simulated: Armed perimeter CCTV tripwires")
        if not simulated_list:
            simulated_list.append(f"Simulated routine execution for {automation.name}")

        # Record activity event
        event = SecurityEvent(
            household_id=household_id,
            event_type="system_status",
            severity="informational",
            title=f"Routine Executed: {automation.name}",
            description="; ".join(simulated_list),
            source="simulated",
            is_acknowledged=True,
            created_at=datetime.now(timezone.utc)
        )
        db.add(event)

        # Record notification
        notif = Notification(
            household_id=household_id,
            title=f"Automation Triggered: {automation.name}",
            message="; ".join(simulated_list),
            notification_type="routine",
            is_read=False,
            created_at=datetime.now(timezone.utc)
        )
        db.add(notif)
        db.commit()

        return AutomationTestResult(
            automation_id=automation.id,
            name=automation.name,
            status="success",
            simulated_actions=simulated_list,
            message="Automation test routine completed successfully."
        )
