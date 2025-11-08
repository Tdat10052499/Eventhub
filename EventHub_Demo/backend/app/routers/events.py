"""
Event Router
CRUD operations for events
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.database import get_db
from app.utils.auth import get_current_user, require_admin, Auth0User
from app.utils import crud_events
from app.schemas import EventResponse, EventCreate, EventUpdate, EventWithTeambuilding


router = APIRouter()


@router.get("/", response_model=List[EventResponse])
async def get_events(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    teambuilding_id: Optional[int] = Query(None),
    status: Optional[str] = Query(None),
    search: Optional[str] = Query(None),
    db: Session = Depends(get_db),
    current_user: Auth0User = Depends(get_current_user)
):
    """Get list of events"""
    events = crud_events.get_events(
        db,
        skip=skip,
        limit=limit,
        teambuilding_id=teambuilding_id,
        status=status,
        search=search
    )
    return events


@router.get("/upcoming", response_model=List[EventResponse])
async def get_upcoming_events(
    limit: int = Query(10, ge=1, le=50),
    db: Session = Depends(get_db),
    current_user: Auth0User = Depends(get_current_user)
):
    """Get upcoming events"""
    events = crud_events.get_upcoming_events(db, limit=limit)
    return events


@router.get("/{event_id}", response_model=EventWithTeambuilding)
async def get_event(
    event_id: int,
    db: Session = Depends(get_db),
    current_user: Auth0User = Depends(get_current_user)
):
    """Get event by ID with teambuilding info"""
    event = crud_events.get_event(db, event_id)
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event not found"
        )
    return event


@router.post("/", response_model=EventResponse, status_code=status.HTTP_201_CREATED)
async def create_event(
    event: EventCreate,
    db: Session = Depends(get_db),
    current_user: Auth0User = Depends(require_admin)
):
    """Create new event (Admin only)"""
    new_event = crud_events.create_event(db, event)
    return new_event


@router.put("/{event_id}", response_model=EventResponse)
async def update_event(
    event_id: int,
    event_update: EventUpdate,
    db: Session = Depends(get_db),
    current_user: Auth0User = Depends(require_admin)
):
    """Update event (Admin only)"""
    updated_event = crud_events.update_event(db, event_id, event_update)
    if not updated_event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event not found"
        )
    return updated_event


@router.delete("/{event_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_event(
    event_id: int,
    db: Session = Depends(get_db),
    current_user: Auth0User = Depends(require_admin)
):
    """Delete event (Admin only)"""
    success = crud_events.delete_event(db, event_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event not found"
        )
    return None


@router.get("/{event_id}/availability", response_model=dict)
async def check_event_availability(
    event_id: int,
    db: Session = Depends(get_db),
    current_user: Auth0User = Depends(get_current_user)
):
    """Check if event has available slots"""
    available = crud_events.check_event_availability(db, event_id)
    event = crud_events.get_event(db, event_id)
    
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event not found"
        )
    
    return {
        "event_id": event_id,
        "available": available,
        "max_participants": event.max_participants,
        "current_participants": event.current_participants,
        "slots_remaining": event.max_participants - event.current_participants if event.max_participants else None
    }
