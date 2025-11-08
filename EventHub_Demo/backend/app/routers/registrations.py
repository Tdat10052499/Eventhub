"""
Registration Router
CRUD operations for event registrations
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.database import get_db
from app.utils.auth import get_current_user, require_admin, Auth0User
from app.utils import crud_registrations, crud_users
from app.schemas import RegistrationResponse, RegistrationCreate, RegistrationUpdate, RegistrationWithDetails


router = APIRouter()


@router.get("/", response_model=List[RegistrationWithDetails])
async def get_registrations(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    event_id: Optional[int] = Query(None),
    status: Optional[str] = Query(None),
    db: Session = Depends(get_db),
    current_user: Auth0User = Depends(require_admin)
):
    """Get list of all registrations (Admin only)"""
    registrations = crud_registrations.get_registrations(
        db,
        skip=skip,
        limit=limit,
        event_id=event_id,
        status=status
    )
    return registrations


@router.get("/my-registrations", response_model=List[RegistrationWithDetails])
async def get_my_registrations(
    status: Optional[str] = Query(None),
    db: Session = Depends(get_db),
    current_user: Auth0User = Depends(get_current_user)
):
    """Get current user's registrations"""
    # Get user from database
    db_user = crud_users.get_user_by_auth0_id(db, current_user.sub)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    registrations = crud_registrations.get_user_registrations(db, db_user.id, status=status)
    return registrations


@router.get("/event/{event_id}", response_model=List[RegistrationWithDetails])
async def get_event_registrations(
    event_id: int,
    status: Optional[str] = Query(None),
    db: Session = Depends(get_db),
    current_user: Auth0User = Depends(require_admin)
):
    """Get registrations for a specific event (Admin only)"""
    registrations = crud_registrations.get_event_registrations(db, event_id, status=status)
    return registrations


@router.get("/{registration_id}", response_model=RegistrationWithDetails)
async def get_registration(
    registration_id: int,
    db: Session = Depends(get_db),
    current_user: Auth0User = Depends(get_current_user)
):
    """Get registration by ID"""
    registration = crud_registrations.get_registration(db, registration_id)
    if not registration:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Registration not found"
        )
    
    # Check if user owns this registration or is admin
    db_user = crud_users.get_user_by_auth0_id(db, current_user.sub)
    if db_user and registration.user_id != db_user.id:
        # Not owner, check if admin
        if "admin" not in current_user.permissions:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to view this registration"
            )
    
    return registration


@router.post("/", response_model=RegistrationResponse, status_code=status.HTTP_201_CREATED)
async def create_registration(
    registration: RegistrationCreate,
    db: Session = Depends(get_db),
    current_user: Auth0User = Depends(get_current_user)
):
    """Create new registration"""
    # Get or create user
    db_user = crud_users.get_or_create_user(
        db,
        auth0_id=current_user.sub,
        email=current_user.email,
        name=current_user.name
    )
    
    try:
        new_registration = crud_registrations.create_registration(db, registration, db_user.id)
        return new_registration
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.put("/{registration_id}", response_model=RegistrationResponse)
async def update_registration(
    registration_id: int,
    registration_update: RegistrationUpdate,
    db: Session = Depends(get_db),
    current_user: Auth0User = Depends(require_admin)
):
    """Update registration status (Admin only)"""
    updated_registration = crud_registrations.update_registration(db, registration_id, registration_update)
    if not updated_registration:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Registration not found"
        )
    return updated_registration


@router.delete("/{registration_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_registration(
    registration_id: int,
    db: Session = Depends(get_db),
    current_user: Auth0User = Depends(get_current_user)
):
    """Delete/cancel registration"""
    registration = crud_registrations.get_registration(db, registration_id)
    if not registration:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Registration not found"
        )
    
    # Check if user owns this registration or is admin
    db_user = crud_users.get_user_by_auth0_id(db, current_user.sub)
    if db_user and registration.user_id != db_user.id:
        if "admin" not in current_user.permissions:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to delete this registration"
            )
    
    success = crud_registrations.delete_registration(db, registration_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Registration not found"
        )
    return None
