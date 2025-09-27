from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
import uuid

from database import get_database
from schemas import CounsellingSession, CounsellingSessionCreate, CounsellingSessionUpdate
import crud

router = APIRouter(prefix="/api/counselling", tags=["counselling"])

@router.get("/{student_id}", response_model=List[CounsellingSession])
async def get_student_counselling_sessions(student_id: uuid.UUID, db: AsyncSession = Depends(get_database)):
    """Get all counselling sessions for a specific student"""
    return await crud.get_counselling_sessions_by_student(db, student_id=student_id)

@router.post("/", response_model=CounsellingSession)
async def create_counselling_session(session: CounsellingSessionCreate, db: AsyncSession = Depends(get_database)):
    """Create a new counselling session"""
    return await crud.create_counselling_session(db, session=session)

@router.patch("/{session_id}", response_model=CounsellingSession)
async def update_counselling_session(
    session_id: uuid.UUID,
    session_update: CounsellingSessionUpdate,
    db: AsyncSession = Depends(get_database)
):
    """Update a counselling session"""
    session = await crud.update_counselling_session(db, session_id=session_id, session_update=session_update)
    if session is None:
        raise HTTPException(status_code=404, detail="Counselling session not found")
    return session