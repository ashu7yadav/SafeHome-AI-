from typing import List, Optional
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.user import User
from app.schemas.notification import NotificationResponse, UnreadCountResponse
from app.services.notification_service import NotificationService
from app.api.deps import get_current_user

router = APIRouter(prefix="/notifications", tags=["Notifications"])


@router.get("", response_model=List[NotificationResponse])
def get_notifications(
    is_read: Optional[bool] = None,
    limit: int = 50,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return NotificationService.get_notifications(db, current_user.household_id, is_read, limit)


@router.get("/unread-count", response_model=UnreadCountResponse)
def get_unread_count(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    count = NotificationService.get_unread_count(db, current_user.household_id)
    return UnreadCountResponse(unread_count=count)


@router.patch("/{notification_id}/read", response_model=NotificationResponse)
def mark_notification_read(
    notification_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return NotificationService.mark_as_read(db, current_user.household_id, notification_id)


@router.patch("/read-all")
def mark_all_notifications_read(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    count = NotificationService.mark_all_as_read(db, current_user.household_id)
    return {"message": f"Marked {count} notifications as read", "count": count}


@router.delete("/{notification_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_notification(
    notification_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    NotificationService.delete_notification(db, current_user.household_id, notification_id)
