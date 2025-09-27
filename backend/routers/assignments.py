from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
import uuid

from database import get_database
from schemas import Assignment, AssignmentCreate, AssignmentUpdate
import crud

router = APIRouter(prefix="/api/assignments", tags=["assignments"])

@router.get("/{student_id}", response_model=List[Assignment])
async def get_student_assignments(student_id: uuid.UUID, db: AsyncSession = Depends(get_database)):
    """Get all assignments for a specific student"""
    return await crud.get_assignments_by_student(db, student_id=student_id)

@router.post("/", response_model=Assignment)
async def create_assignment(assignment: AssignmentCreate, db: AsyncSession = Depends(get_database)):
    """Create a new assignment"""
    return await crud.create_assignment(db, assignment=assignment)