"""
Database CRUD operations for Registrations
"""

from sqlalchemy.orm import Session
from sqlalchemy import func, and_
from typing import Optional, List

from app.models import Registration, RegistrationStatus, Event
from app.schemas import RegistrationCreate, RegistrationUpdate


def get_registration(db: Session, registration_id: int) -> Optional[Registration]:
    """Get registration by ID"""
    return db.query(Registration).filter(Registration.id == registration_id).first()


def get_registrations(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    event_id: Optional[int] = None,
    user_id: Optional[int] = None,
    status: Optional[str] = None
) -> List[Registration]:
    """Get list of registrations with filters"""
    query = db.query(Registration)
    
    if event_id:
        query = query.filter(Registration.event_id == event_id)
    
    if user_id:
        query = query.filter(Registration.user_id == user_id)
    
    if status:
        query = query.filter(Registration.status == status)
    
    return query.order_by(Registration.registration_date.desc()).offset(skip).limit(limit).all()


def create_registration(db: Session, registration: RegistrationCreate, user_id: int) -> Registration:
    """Create new registration"""
    # Check if already registered
    existing = db.query(Registration).filter(
        and_(
            Registration.event_id == registration.event_id,
            Registration.user_id == user_id
        )
    ).first()
    
    if existing:
        raise ValueError("User already registered for this event")
    
    # Check event availability
    event = db.query(Event).filter(Event.id == registration.event_id).first()
    if not event:
        raise ValueError("Event not found")
    
    if event.max_participants is not None and event.current_participants >= event.max_participants:
        raise ValueError("Event is full")
    
    # Create registration
    db_registration = Registration(
        event_id=registration.event_id,
        user_id=user_id,
        notes=registration.notes,
        status=RegistrationStatus.PENDING
    )
    db.add(db_registration)
    db.commit()
    db.refresh(db_registration)
    return db_registration


def update_registration(
    db: Session,
    registration_id: int,
    registration_update: RegistrationUpdate
) -> Optional[Registration]:
    """Update registration (mainly status)"""
    db_registration = get_registration(db, registration_id)
    if not db_registration:
        return None
    
    old_status = db_registration.status
    update_data = registration_update.model_dump(exclude_unset=True)
    
    for field, value in update_data.items():
        if field == "status":
            setattr(db_registration, field, RegistrationStatus(value))
        else:
            setattr(db_registration, field, value)
    
    new_status = db_registration.status
    
    # Update event participant count
    # Note: This is also handled by database trigger, but we do it here for consistency
    if old_status != new_status:
        event = db.query(Event).filter(Event.id == db_registration.event_id).first()
        if event:
            if old_status != RegistrationStatus.CONFIRMED and new_status == RegistrationStatus.CONFIRMED:
                event.current_participants += 1
            elif old_status == RegistrationStatus.CONFIRMED and new_status != RegistrationStatus.CONFIRMED:
                event.current_participants = max(0, event.current_participants - 1)
    
    db.commit()
    db.refresh(db_registration)
    return db_registration


def delete_registration(db: Session, registration_id: int) -> bool:
    """Delete registration"""
    db_registration = get_registration(db, registration_id)
    if not db_registration:
        return False
    
    # Update event participant count if confirmed
    if db_registration.status == RegistrationStatus.CONFIRMED:
        event = db.query(Event).filter(Event.id == db_registration.event_id).first()
        if event:
            event.current_participants = max(0, event.current_participants - 1)
    
    db.delete(db_registration)
    db.commit()
    return True


def get_user_registrations(db: Session, user_id: int, status: Optional[str] = None) -> List[Registration]:
    """Get all registrations for a user"""
    query = db.query(Registration).filter(Registration.user_id == user_id)
    
    if status:
        query = query.filter(Registration.status == status)
    
    return query.order_by(Registration.registration_date.desc()).all()


def get_event_registrations(db: Session, event_id: int, status: Optional[str] = None) -> List[Registration]:
    """Get all registrations for an event"""
    query = db.query(Registration).filter(Registration.event_id == event_id)
    
    if status:
        query = query.filter(Registration.status == status)
    
    return query.order_by(Registration.registration_date.desc()).all()


def count_registrations(db: Session, status: Optional[str] = None) -> int:
    """Count registrations"""
    query = db.query(func.count(Registration.id))
    if status:
        query = query.filter(Registration.status == status)
    return query.scalar()


def check_user_registered(db: Session, user_id: int, event_id: int) -> bool:
    """Check if user is registered for an event"""
    return db.query(Registration).filter(
        and_(
            Registration.user_id == user_id,
            Registration.event_id == event_id
        )
    ).first() is not None
