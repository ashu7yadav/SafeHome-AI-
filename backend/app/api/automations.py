from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.user import User
from app.schemas.automation import (
    AutomationCreate, 
    AutomationUpdate, 
    AutomationResponse, 
    AutomationTestResult
)
from app.services.automation_service import AutomationService
from app.api.deps import get_current_user

router = APIRouter(prefix="/automations", tags=["Automations"])


@router.get("", response_model=List[AutomationResponse])
def get_automations(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return AutomationService.get_automations(db, current_user.household_id)


@router.post("", response_model=AutomationResponse, status_code=status.HTTP_201_CREATED)
def create_automation(
    automation_in: AutomationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return AutomationService.create_automation(db, current_user.household_id, automation_in)


@router.get("/{automation_id}", response_model=AutomationResponse)
def get_automation(
    automation_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return AutomationService.get_automation(db, current_user.household_id, automation_id)


@router.patch("/{automation_id}", response_model=AutomationResponse)
def update_automation(
    automation_id: str,
    automation_in: AutomationUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return AutomationService.update_automation(db, current_user.household_id, automation_id, automation_in)


@router.patch("/{automation_id}/toggle", response_model=AutomationResponse)
def toggle_automation(
    automation_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return AutomationService.toggle_automation(db, current_user.household_id, automation_id)


@router.delete("/{automation_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_automation(
    automation_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    AutomationService.delete_automation(db, current_user.household_id, automation_id)


@router.post("/{automation_id}/test", response_model=AutomationTestResult)
def test_automation_routine(
    automation_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return AutomationService.test_automation(db, current_user.household_id, automation_id)
