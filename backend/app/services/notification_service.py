from typing import List, Optional
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.notification import Notification


class NotificationService:
    @staticmethod
    def get_notifications(
        db: Session, 
        household_id: str, 
        is_read: Optional[bool] = None, 
        limit: int = 50
    ) -> List[Notification]:
        query = db.query(Notification).filter(Notification.household_id == household_id)
        if is_read is not None:
            query = query.filter(Notification.is_read == is_read)
        return query.order_by(Notification.created_at.desc()).limit(limit).all()

    @staticmethod
    def get_unread_count(db: Session, household_id: str) -> int:
        return db.query(Notification).filter(
            Notification.household_id == household_id,
            Notification.is_read == False
        ).count()

    @staticmethod
    def mark_as_read(db: Session, household_id: str, notification_id: str) -> Notification:
        notification = db.query(Notification).filter(
            Notification.id == notification_id,
            Notification.household_id == household_id
        ).first()
        if not notification:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Notification not found")
        notification.is_read = True
        db.commit()
        db.refresh(notification)
        return notification

    @staticmethod
    def mark_all_as_read(db: Session, household_id: str) -> int:
        count = db.query(Notification).filter(
            Notification.household_id == household_id,
            Notification.is_read == False
        ).update({Notification.is_read: True})
        db.commit()
        return count

    @staticmethod
    def delete_notification(db: Session, household_id: str, notification_id: str) -> None:
        notification = db.query(Notification).filter(
            Notification.id == notification_id,
            Notification.household_id == household_id
        ).first()
        if not notification:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Notification not found")
        db.delete(notification)
        db.commit()
