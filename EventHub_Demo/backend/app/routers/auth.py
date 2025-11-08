"""
Authentication Router
Handles user authentication and profile
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.utils.auth import get_current_user, Auth0User
from app.utils import crud_users
from app.schemas import UserResponse, UserUpdate


router = APIRouter()


@router.get("/me", response_model=UserResponse)
async def get_my_profile(
    current_user: Auth0User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get current user profile"""
    # Get or create user in database
    db_user = crud_users.get_or_create_user(
        db,
        auth0_id=current_user.sub,
        email=current_user.email,
        name=current_user.name
    )
    return db_user


@router.put("/me", response_model=UserResponse)
async def update_my_profile(
    user_update: UserUpdate,
    current_user: Auth0User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update current user profile"""
    db_user = crud_users.get_user_by_auth0_id(db, current_user.sub)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    updated_user = crud_users.update_user(db, db_user.id, user_update)
    return updated_user
