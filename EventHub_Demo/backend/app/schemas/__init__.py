"""
Pydantic Schemas for Request/Response validation
"""

from __future__ import annotations  # Enable forward references

from pydantic import BaseModel, EmailStr, Field, ConfigDict
from typing import Optional, List
from datetime import datetime, date
from decimal import Decimal


# ============ User Schemas ============
class UserBase(BaseModel):
    email: EmailStr
    name: str
    phone: Optional[str] = None
    avatar_url: Optional[str] = None


class UserCreate(UserBase):
    auth0_id: str
    role: str = "user"


class UserUpdate(BaseModel):
    name: Optional[str] = None
    phone: Optional[str] = None
    avatar_url: Optional[str] = None


class UserResponse(UserBase):
    id: int
    auth0_id: str
    role: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


# ============ Teambuilding Schemas ============
class TeambuildingBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    start_date: date
    end_date: date
    location: Optional[str] = None
    budget: Optional[Decimal] = None
    status: str = "active"


class TeambuildingCreate(TeambuildingBase):
    image_url: Optional[str] = None


class TeambuildingUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    location: Optional[str] = None
    budget: Optional[Decimal] = None
    image_url: Optional[str] = None
    status: Optional[str] = None


class TeambuildingResponse(TeambuildingBase):
    id: int
    image_url: Optional[str] = None
    created_by: Optional[int] = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


# ============ Event Schemas ============
class EventBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    event_date: datetime
    location: Optional[str] = None
    max_participants: Optional[int] = Field(None, gt=0)


class EventCreate(EventBase):
    teambuilding_id: int
    image_url: Optional[str] = None


class EventUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    event_date: Optional[datetime] = None
    location: Optional[str] = None
    max_participants: Optional[int] = Field(None, gt=0)
    image_url: Optional[str] = None
    status: Optional[str] = None


class EventResponse(EventBase):
    id: int
    teambuilding_id: int
    image_url: Optional[str] = None
    current_participants: int
    status: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class EventWithTeambuilding(EventResponse):
    teambuilding: Optional[TeambuildingResponse] = None


# Define after EventResponse is created
class TeambuildingWithEvents(TeambuildingResponse):
    events: List[EventResponse] = []


# ============ Registration Schemas ============
class RegistrationBase(BaseModel):
    notes: Optional[str] = None


class RegistrationCreate(RegistrationBase):
    event_id: int


class RegistrationUpdate(BaseModel):
    status: str
    notes: Optional[str] = None


class RegistrationResponse(RegistrationBase):
    id: int
    event_id: int
    user_id: int
    registration_date: datetime
    status: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class RegistrationWithDetails(RegistrationResponse):
    event: Optional[EventResponse] = None
    user: Optional[UserResponse] = None


# ============ Upload Schemas ============
class ImageUploadResponse(BaseModel):
    filename: str
    url: str
    size: int


# ============ Statistics Schemas ============
class DashboardStats(BaseModel):
    total_teambuildings: int
    total_events: int
    total_registrations: int
    total_users: int
    upcoming_events: int
    active_teambuildings: int
