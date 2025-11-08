"""
Database CRUD operations for Teambuildings
"""

from sqlalchemy.orm import Session
from sqlalchemy import func, or_
from typing import Optional, List
from datetime import date

from app.models import Teambuilding
from app.schemas import TeambuildingCreate, TeambuildingUpdate


def get_teambuilding(db: Session, teambuilding_id: int) -> Optional[Teambuilding]:
    """Get teambuilding by ID"""
    return db.query(Teambuilding).filter(Teambuilding.id == teambuilding_id).first()


def get_teambuildings(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    status: Optional[str] = None,
    search: Optional[str] = None
) -> List[Teambuilding]:
    """Get list of teambuildings with filters"""
    query = db.query(Teambuilding)
    
    if status:
        query = query.filter(Teambuilding.status == status)
    
    if search:
        query = query.filter(
            or_(
                Teambuilding.name.ilike(f"%{search}%"),
                Teambuilding.location.ilike(f"%{search}%")
            )
        )
    
    return query.order_by(Teambuilding.start_date.desc()).offset(skip).limit(limit).all()


def create_teambuilding(db: Session, teambuilding: TeambuildingCreate, created_by: int) -> Teambuilding:
    """Create new teambuilding"""
    db_teambuilding = Teambuilding(
        **teambuilding.model_dump(),
        created_by=created_by
    )
    db.add(db_teambuilding)
    db.commit()
    db.refresh(db_teambuilding)
    return db_teambuilding


def update_teambuilding(
    db: Session,
    teambuilding_id: int,
    teambuilding_update: TeambuildingUpdate
) -> Optional[Teambuilding]:
    """Update teambuilding"""
    db_teambuilding = get_teambuilding(db, teambuilding_id)
    if not db_teambuilding:
        return None
    
    update_data = teambuilding_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_teambuilding, field, value)
    
    db.commit()
    db.refresh(db_teambuilding)
    return db_teambuilding


def delete_teambuilding(db: Session, teambuilding_id: int) -> bool:
    """Delete teambuilding"""
    db_teambuilding = get_teambuilding(db, teambuilding_id)
    if not db_teambuilding:
        return False
    
    db.delete(db_teambuilding)
    db.commit()
    return True


def get_active_teambuildings(db: Session) -> List[Teambuilding]:
    """Get active teambuildings (end_date >= today)"""
    today = date.today()
    return db.query(Teambuilding).filter(
        Teambuilding.status == "active",
        Teambuilding.end_date >= today
    ).order_by(Teambuilding.start_date).all()


def count_teambuildings(db: Session, status: Optional[str] = None) -> int:
    """Count teambuildings"""
    query = db.query(func.count(Teambuilding.id))
    if status:
        query = query.filter(Teambuilding.status == status)
    return query.scalar()
