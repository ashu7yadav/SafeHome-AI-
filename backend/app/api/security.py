from typing import List, Optional
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.user import User
from app.schemas.event import (
    SecurityEventDemo, 
    SecurityEventAcknowledge, 
    SecurityEventResponse
)
from app.services.security_service import SecurityService
from app.api.deps import get_current_user

router = APIRouter(prefix="/security", tags=["Security & Events"])


@router.get("/events", response_model=List[SecurityEventResponse])
def get_security_events(
    severity: Optional[str] = None,
    event_type: Optional[str] = None,
    is_acknowledged: Optional[bool] = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return SecurityService.get_events(
        db=db,
        household_id=current_user.household_id,
        severity=severity,
        event_type=event_type,
        is_acknowledged=is_acknowledged,
        skip=skip,
        limit=limit
    )


@router.get("/events/{event_id}", response_model=SecurityEventResponse)
def get_security_event(
    event_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return SecurityService.get_event(db, current_user.household_id, event_id)


@router.post("/events/demo", response_model=SecurityEventResponse, status_code=status.HTTP_201_CREATED)
def trigger_demo_security_event(
    payload: SecurityEventDemo,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return SecurityService.create_demo_event(db, current_user.household_id, payload)


@router.patch("/events/{event_id}/acknowledge", response_model=SecurityEventResponse)
def acknowledge_security_event(
    event_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return SecurityService.acknowledge_event(
        db, 
        current_user.household_id, 
        event_id, 
        current_user.full_name
    )


@router.post("/events/acknowledge-all")
def acknowledge_all_security_events(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    count = SecurityService.acknowledge_all_events(
        db, 
        current_user.household_id, 
        current_user.full_name
    )
    return {"message": f"Successfully acknowledged {count} alerts", "count": count}


@router.get("/status")
def get_overall_security_status(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return SecurityService.get_security_status(db, current_user.household_id)
