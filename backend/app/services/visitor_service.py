from datetime import datetime, timezone
from typing import List, Optional
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.visitor import Visitor
from app.schemas.visitor import VisitorCreate, VisitorUpdate


class VisitorService:
    @staticmethod
    def get_visitors(db: Session, household_id: str, status_filter: Optional[str] = None) -> List[Visitor]:
        query = db.query(Visitor).filter(Visitor.household_id == household_id)
        if status_filter:
            query = query.filter(Visitor.access_status == status_filter)
        return query.order_by(Visitor.created_at.desc()).all()

    @staticmethod
    def get_visitor(db: Session, household_id: str, visitor_id: str) -> Visitor:
        visitor = db.query(Visitor).filter(
            Visitor.id == visitor_id,
            Visitor.household_id == household_id
        ).first()
        if not visitor:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Visitor not found")
        return visitor

    @staticmethod
    def create_visitor(db: Session, household_id: str, obj_in: VisitorCreate, user_name: str) -> Visitor:
        visitor = Visitor(
            household_id=household_id,
            visitor_name=obj_in.visitor_name,
            contact_information=obj_in.contact_information,
            purpose=obj_in.purpose,
            access_status="approved",
            valid_from=obj_in.valid_from or datetime.now(timezone.utc),
            valid_until=obj_in.valid_until,
            approved_by=user_name,
            created_at=datetime.now(timezone.utc)
        )
        db.add(visitor)
        db.commit()
        db.refresh(visitor)
        return visitor

    @staticmethod
    def update_visitor(db: Session, household_id: str, visitor_id: str, obj_in: VisitorUpdate) -> Visitor:
        visitor = db.query(Visitor).filter(
            Visitor.id == visitor_id,
            Visitor.household_id == household_id
        ).first()
        if not visitor:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Visitor not found")

        update_data = obj_in.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(visitor, field, value)

        db.commit()
        db.refresh(visitor)
        return visitor

    @staticmethod
    def approve_visitor(db: Session, household_id: str, visitor_id: str, user_name: str) -> Visitor:
        visitor = db.query(Visitor).filter(
            Visitor.id == visitor_id,
            Visitor.household_id == household_id
        ).first()
        if not visitor:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Visitor not found")

        visitor.access_status = "approved"
        visitor.approved_by = user_name
        db.commit()
        db.refresh(visitor)
        return visitor

    @staticmethod
    def revoke_visitor(db: Session, household_id: str, visitor_id: str) -> Visitor:
        visitor = db.query(Visitor).filter(
            Visitor.id == visitor_id,
            Visitor.household_id == household_id
        ).first()
        if not visitor:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Visitor not found")

        visitor.access_status = "revoked"
        db.commit()
        db.refresh(visitor)
        return visitor

    @staticmethod
    def delete_visitor(db: Session, household_id: str, visitor_id: str) -> None:
        visitor = db.query(Visitor).filter(
            Visitor.id == visitor_id,
            Visitor.household_id == household_id
        ).first()
        if not visitor:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Visitor not found")
        db.delete(visitor)
        db.commit()
