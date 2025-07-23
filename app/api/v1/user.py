from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from core.database import get_db
from sqlalchemy import text

router = APIRouter(prefix="users")

@router