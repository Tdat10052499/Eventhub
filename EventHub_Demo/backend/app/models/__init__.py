"""
SQLAlchemy Database Models
Mapping to PostgreSQL tables
"""

from sqlalchemy import Column, Integer, String, Text, Date, DateTime, Numeric, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum

from app.database import Base


# Enums
class UserRole(str, enum.Enum):
    ADMIN = "admin"
    USER = "user"
    
    def __str__(self):
        return self.value


class RegistrationStatus(str, enum.Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    CANCELLED = "cancelled"
    
    def __str__(self):
        return self.value


# Models
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    auth0_id = Column(String(255), unique=True, nullable=False, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    name = Column(String(255), nullable=False)
    role = Column(SQLEnum(UserRole, values_callable=lambda obj: [e.value for e in obj]), nullable=False, default=UserRole.USER)
    avatar_url = Column(String(500))
    phone = Column(String(20))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    created_teambuildings = relationship("Teambuilding", back_populates="creator")
    registrations = relationship("Registration", back_populates="user")


class Teambuilding(Base):
    __tablename__ = "teambuildings"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    location = Column(String(255))
    image_url = Column(String(500))
    budget = Column(Numeric(12, 2))
    status = Column(String(50), default="active")
    created_by = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    creator = relationship("User", back_populates="created_teambuildings")
    events = relationship("Event", back_populates="teambuilding", cascade="all, delete-orphan")


class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True)
    teambuilding_id = Column(Integer, ForeignKey("teambuildings.id", ondelete="CASCADE"), nullable=False)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    event_date = Column(DateTime(timezone=True), nullable=False)
    location = Column(String(255))
    image_url = Column(String(500))
    max_participants = Column(Integer)
    current_participants = Column(Integer, default=0)
    status = Column(String(50), default="open")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    teambuilding = relationship("Teambuilding", back_populates="events")
    registrations = relationship("Registration", back_populates="event", cascade="all, delete-orphan")


class Registration(Base):
    __tablename__ = "registrations"

    id = Column(Integer, primary_key=True, index=True)
    event_id = Column(Integer, ForeignKey("events.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    registration_date = Column(DateTime(timezone=True), server_default=func.now())
    status = Column(SQLEnum(RegistrationStatus, values_callable=lambda obj: [e.value for e in obj]), nullable=False, default=RegistrationStatus.PENDING)
    notes = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    event = relationship("Event", back_populates="registrations")
    user = relationship("User", back_populates="registrations")
