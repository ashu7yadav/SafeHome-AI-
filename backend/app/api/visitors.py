from typing import List, Optional
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.user import User
from app.schemas.visitor import VisitorCreate, VisitorUpdate, VisitorResponse
from app.services.visitor_service import VisitorService
from app.api.deps import get_current_user

router = APIRouter(prefix="/visitors", tags=["Visitor Management"])


@router.get("", response_model=List[VisitorResponse])
def get_visitors(
    status: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return VisitorService.get_visitors(db, current_user.household_id, status)


@router.post("", response_model=VisitorResponse, status_code=status.HTTP_201_CREATED)
def create_visitor(
    visitor_in: VisitorCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return VisitorService.create_visitor(
        db, 
        current_user.household_id, 
        visitor_in, 
        current_user.full_name
    )


@router.get("/{visitor_id}", response_model=VisitorResponse)
def get_visitor(
    visitor_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return VisitorService.get_visitor(db, current_user.household_id, visitor_id)


@router.patch("/{visitor_id}", response_model=VisitorResponse)
def update_visitor(
    visitor_id: str,
    visitor_in: VisitorUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return VisitorService.update_visitor(db, current_user.household_id, visitor_id, visitor_in)


@router.patch("/{visitor_id}/approve", response_model=VisitorResponse)
def approve_visitor(
    visitor_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return VisitorService.approve_visitor(
        db, 
        current_user.household_id, 
        visitor_id, 
        current_user.full_name
    )


@router.patch("/{visitor_id}/revoke", response_model=VisitorResponse)
def revoke_visitor(
    visitor_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return VisitorService.revoke_visitor(db, current_user.household_id, visitor_id)


@router.delete("/{visitor_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_visitor(
    visitor_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    VisitorService.delete_visitor(db, current_user.household_id, visitor_id)
