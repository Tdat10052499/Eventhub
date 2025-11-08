"""
Database CRUD operations for Users
"""

from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import Optional, List

from app.models import User, UserRole
from app.schemas import UserCreate, UserUpdate


def get_user_by_id(db: Session, user_id: int) -> Optional[User]:
    """Get user by ID"""
    return db.query(User).filter(User.id == user_id).first()


def get_user_by_auth0_id(db: Session, auth0_id: str) -> Optional[User]:
    """Get user by Auth0 ID"""
    return db.query(User).filter(User.auth0_id == auth0_id).first()


def get_user_by_email(db: Session, email: str) -> Optional[User]:
    """Get user by email"""
    return db.query(User).filter(User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100, role: Optional[str] = None) -> List[User]:
    """Get list of users with pagination"""
    query = db.query(User)
    
    if role:
        query = query.filter(User.role == role)
    
    return query.offset(skip).limit(limit).all()


def create_user(db: Session, user: UserCreate) -> User:
    """Create new user"""
    db_user = User(
        auth0_id=user.auth0_id,
        email=user.email,
        name=user.name,
        role=UserRole(user.role),
        phone=user.phone,
        avatar_url=user.avatar_url
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def update_user(db: Session, user_id: int, user_update: UserUpdate) -> Optional[User]:
    """Update user information"""
    db_user = get_user_by_id(db, user_id)
    if not db_user:
        return None
    
    update_data = user_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_user, field, value)
    
    db.commit()
    db.refresh(db_user)
    return db_user


def delete_user(db: Session, user_id: int) -> bool:
    """Delete user"""
    db_user = get_user_by_id(db, user_id)
    if not db_user:
        return False
    
    db.delete(db_user)
    db.commit()
    return True


def get_or_create_user(db: Session, auth0_id: str, email: str, name: str, role: str = "user") -> User:
    """Get existing user or create new one"""
    user = get_user_by_auth0_id(db, auth0_id)
    if user:
        # Update role if different
        if user.role != role:
            user.role = UserRole(role)
            db.commit()
            db.refresh(user)
        return user
    
    # Create new user
    user_create = UserCreate(
        auth0_id=auth0_id,
        email=email,
        name=name,
        role=role
    )
    return create_user(db, user_create)


def count_users(db: Session) -> int:
    """Count total users"""
    return db.query(func.count(User.id)).scalar()
