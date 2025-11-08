"""
Dashboard Router
Statistics and dashboard data
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.utils.auth import require_admin, Auth0User
from app.utils import crud_teambuildings, crud_events, crud_registrations, crud_users
from app.schemas import DashboardStats


router = APIRouter()


@router.get("/stats", response_model=DashboardStats)
async def get_dashboard_stats(
    db: Session = Depends(get_db),
    current_user: Auth0User = Depends(require_admin)
):
    """Get dashboard statistics (Admin only)"""
    total_teambuildings = crud_teambuildings.count_teambuildings(db)
    total_events = crud_events.count_events(db)
    total_registrations = crud_registrations.count_registrations(db)
    total_users = crud_users.count_users(db)
    upcoming_events = crud_events.count_upcoming_events(db)
    active_teambuildings = crud_teambuildings.count_teambuildings(db, status="active")
    
    return DashboardStats(
        total_teambuildings=total_teambuildings,
        total_events=total_events,
        total_registrations=total_registrations,
        total_users=total_users,
        upcoming_events=upcoming_events,
        active_teambuildings=active_teambuildings
    )
