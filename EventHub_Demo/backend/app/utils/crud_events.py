"""
Database CRUD operations for Events
"""

from sqlalchemy.orm import Session
from sqlalchemy import func, or_, and_
from typing import Optional, List
from datetime import datetime

from app.models import Event
from app.schemas import EventCreate, EventUpdate


def get_event(db: Session, event_id: int) -> Optional[Event]:
    """Get event by ID"""
    return db.query(Event).filter(Event.id == event_id).first()


def get_events(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    teambuilding_id: Optional[int] = None,
    status: Optional[str] = None,
    search: Optional[str] = None
) -> List[Event]:
    """Get list of events with filters"""
    query = db.query(Event)
    
    if teambuilding_id:
        query = query.filter(Event.teambuilding_id == teambuilding_id)
    
    if status:
        query = query.filter(Event.status == status)
    
    if search:
        query = query.filter(
            or_(
                Event.name.ilike(f"%{search}%"),
                Event.location.ilike(f"%{search}%")
            )
        )
    
    return query.order_by(Event.event_date.desc()).offset(skip).limit(limit).all()


def create_event(db: Session, event: EventCreate) -> Event:
    """Create new event"""
    db_event = Event(**event.model_dump())
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    return db_event


def update_event(db: Session, event_id: int, event_update: EventUpdate) -> Optional[Event]:
    """Update event"""
    db_event = get_event(db, event_id)
    if not db_event:
        return None
    
    update_data = event_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_event, field, value)
    
    db.commit()
    db.refresh(db_event)
    return db_event


def delete_event(db: Session, event_id: int) -> bool:
    """Delete event"""
    db_event = get_event(db, event_id)
    if not db_event:
        return False
    
    db.delete(db_event)
    db.commit()
    return True


def get_upcoming_events(db: Session, limit: int = 10) -> List[Event]:
    """Get upcoming events (event_date >= now)"""
    now = datetime.now()
    return db.query(Event).filter(
        Event.status == "open",
        Event.event_date >= now
    ).order_by(Event.event_date).limit(limit).all()


def get_events_by_teambuilding(db: Session, teambuilding_id: int) -> List[Event]:
    """Get all events for a teambuilding"""
    return db.query(Event).filter(Event.teambuilding_id == teambuilding_id).order_by(Event.event_date).all()


def check_event_availability(db: Session, event_id: int) -> bool:
    """Check if event has available slots"""
    event = get_event(db, event_id)
    if not event:
        return False
    
    if event.max_participants is None:
        return True  # Unlimited
    
    return event.current_participants < event.max_participants


def count_events(db: Session, status: Optional[str] = None) -> int:
    """Count events"""
    query = db.query(func.count(Event.id))
    if status:
        query = query.filter(Event.status == status)
    return query.scalar()


def count_upcoming_events(db: Session) -> int:
    """Count upcoming events"""
    now = datetime.now()
    return db.query(func.count(Event.id)).filter(
        Event.status == "open",
        Event.event_date >= now
    ).scalar()
