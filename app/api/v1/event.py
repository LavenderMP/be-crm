from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query, BackgroundTasks
from app.schemas.user import UserFilters
from app.core.deps import get_db
from app.models.user import User
from sqlalchemy.orm import Session


router = APIRouter(prefix="/event", tags=["Event"])


def filter_users(filters: UserFilters, db: Session = Depends(get_db)) -> List[User]:
    # Apply filters
    if filters.company:
        query = query.filter(User.company.ilike(f"%{filters.company}%"))
    if filters.job_title:
        query = query.filter(User.job_title.ilike(f"%{filters.job_title}%"))
    if filters.city:
        query = query.filter(User.city.ilike(f"%{filters.city}%"))
    if filters.state:
        query = query.filter(User.state.ilike(f"%{filters.state}%"))

    users = query.all()
    return users


@router.post("/send_emails")
def send_email_to_users(filters: UserFilters, db: Session = Depends(get_db)):
    # Apply same filters as above
    users = filter_users(db=db, filters=filters)
    for user in users:
        # Simulated email
        print(f"Sending email to {user.email}...")
    return {"status": "emails sent", "count": len(users)}
