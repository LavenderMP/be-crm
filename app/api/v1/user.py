from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query, BackgroundTasks
from sqlalchemy.orm import Session
from core.database import get_db
from sqlalchemy import text, func
from serialize.user import UserFilters
from response.user import UserResponse
from models.user import User
from models.event import Event, EventAttendance, EventHost


router = APIRouter(prefix="users", tags=["User"])


@router.get("/", response_model=List[UserResponse])
async def get_users(
    filters: UserFilters = Depends(),
    sort_by: str = Query("last_name", description="Field to sort by"),
    sort_order: str = Query("asc", description="Sort order: asc or desc"),
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
):
    """Get users with filtering, sorting, and pagination"""
    query = db.query(
        User.id,
        User.first_name,
        User.last_name,
        User.email,
        User.company,
        User.job_title,
        User.city,
        User.state,
        # Count subqueries for performance
        db.query(func.count(Event.id))
        .filter(Event.owner_id == User.id)
        .label("hosted_events_count"),
        db.query(func.count(EventAttendance.id))
        .filter(EventAttendance.user_id == User.id)
        .filter(EventAttendance.attended == True)
        .label("attended_events_count"),
    )

    # Apply filters
    if filters.company:
        query = query.filter(User.company.ilike(f"%{filters.company}%"))
    if filters.job_title:
        query = query.filter(User.job_title.ilike(f"%{filters.job_title}%"))
    if filters.city:
        query = query.filter(User.city.ilike(f"%{filters.city}%"))
    if filters.state:
        query = query.filter(User.state.ilike(f"%{filters.state}%"))

    # Apply sorting
    sort_field = getattr(User, sort_by, None)
    if not sort_field:
        sort_field = User.last_name

    if sort_order == "desc":
        query = query.order_by(sort_field.desc())
    else:
        query = query.order_by(sort_field.asc())

    # Apply pagination
    offset = (page - 1) * page_size
    users = query.offset(offset).limit(page_size).all()

    return [
        UserResponse(
            id=user.id,
            first_name=user.first_name,
            last_name=user.last_name,
            email=user.email,
            company=user.company,
            job_title=user.job_title,
            city=user.city,
            state=user.state,
            hosted_events_count=user.hosted_events_count,
            attended_events_count=user.attended_events_count,
        )
        for user in users
    ]
