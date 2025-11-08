"""
Teambuilding Router
CRUD operations for teambuildings
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.database import get_db
from app.utils.auth import get_current_user, require_admin, Auth0User
from app.utils import crud_teambuildings, crud_users
from app.schemas import TeambuildingResponse, TeambuildingCreate, TeambuildingUpdate, TeambuildingWithEvents


router = APIRouter()


@router.get("/", response_model=List[TeambuildingResponse])
async def get_teambuildings(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    status: Optional[str] = Query(None),
    search: Optional[str] = Query(None),
    db: Session = Depends(get_db),
    current_user: Auth0User = Depends(get_current_user)
):
    """Get list of teambuildings"""
    teambuildings = crud_teambuildings.get_teambuildings(db, skip=skip, limit=limit, status=status, search=search)
    return teambuildings


@router.get("/active", response_model=List[TeambuildingResponse])
async def get_active_teambuildings(
    db: Session = Depends(get_db),
    current_user: Auth0User = Depends(get_current_user)
):
    """Get active teambuildings"""
    teambuildings = crud_teambuildings.get_active_teambuildings(db)
    return teambuildings


@router.get("/{teambuilding_id}", response_model=TeambuildingWithEvents)
async def get_teambuilding(
    teambuilding_id: int,
    db: Session = Depends(get_db),
    current_user: Auth0User = Depends(get_current_user)
):
    """Get teambuilding by ID with events"""
    teambuilding = crud_teambuildings.get_teambuilding(db, teambuilding_id)
    if not teambuilding:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Teambuilding not found"
        )
    return teambuilding


@router.post("/", response_model=TeambuildingResponse, status_code=status.HTTP_201_CREATED)
async def create_teambuilding(
    teambuilding: TeambuildingCreate,
    db: Session = Depends(get_db),
    current_user: Auth0User = Depends(require_admin)
):
    """Create new teambuilding (Admin only)"""
    # Get user from database
    db_user = crud_users.get_user_by_auth0_id(db, current_user.sub)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Validate dates
    if teambuilding.end_date < teambuilding.start_date:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="End date must be after start date"
        )
    
    new_teambuilding = crud_teambuildings.create_teambuilding(db, teambuilding, db_user.id)
    return new_teambuilding


@router.put("/{teambuilding_id}", response_model=TeambuildingResponse)
async def update_teambuilding(
    teambuilding_id: int,
    teambuilding_update: TeambuildingUpdate,
    db: Session = Depends(get_db),
    current_user: Auth0User = Depends(require_admin)
):
    """Update teambuilding (Admin only)"""
    # Validate dates if provided
    if teambuilding_update.start_date and teambuilding_update.end_date:
        if teambuilding_update.end_date < teambuilding_update.start_date:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="End date must be after start date"
            )
    
    updated_teambuilding = crud_teambuildings.update_teambuilding(db, teambuilding_id, teambuilding_update)
    if not updated_teambuilding:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Teambuilding not found"
        )
    return updated_teambuilding


@router.delete("/{teambuilding_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_teambuilding(
    teambuilding_id: int,
    db: Session = Depends(get_db),
    current_user: Auth0User = Depends(require_admin)
):
    """Delete teambuilding (Admin only)"""
    success = crud_teambuildings.delete_teambuilding(db, teambuilding_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Teambuilding not found"
        )
    return None
