from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
import uuid

from database import get_database
from schemas import Feedback, FeedbackCreate
import crud

router = APIRouter(prefix="/api/feedback", tags=["feedback"])

@router.get("/{student_id}", response_model=List[Feedback])
async def get_student_feedback(student_id: uuid.UUID, db: AsyncSession = Depends(get_database)):
    """Get all feedback for a specific student"""
    return await crud.get_feedback_by_student(db, student_id=student_id)

@router.post("/", response_model=Feedback)
async def create_feedback(feedback: FeedbackCreate, db: AsyncSession = Depends(get_database)):
    """Create new feedback with sentiment analysis"""
    return await crud.create_feedback(db, feedback=feedback)