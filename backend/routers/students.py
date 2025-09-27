from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
import uuid

from database import get_database
from schemas import Student, StudentCreate, StudentUpdate, StudentSummary
import crud

router = APIRouter(prefix="/api/students", tags=["students"])

@router.get("/", response_model=List[Student])
async def get_students(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_database)):
    """Get all students"""
    return await crud.get_students(db, skip=skip, limit=limit)

@router.get("/{student_id}", response_model=Student)
async def get_student(student_id: uuid.UUID, db: AsyncSession = Depends(get_database)):
    """Get a specific student by ID"""
    student = await crud.get_student(db, student_id=student_id)
    if student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    return student

@router.get("/{student_id}/summary")
async def get_student_summary(student_id: uuid.UUID, db: AsyncSession = Depends(get_database)):
    """Get comprehensive student summary for dashboard"""
    summary = await crud.get_student_summary(db, student_id=student_id)
    if "error" in summary:
        raise HTTPException(status_code=404, detail=summary["error"])
    return summary

@router.post("/", response_model=Student)
async def create_student(student: StudentCreate, db: AsyncSession = Depends(get_database)):
    """Create a new student"""
    # Check if student with roll_no already exists
    existing_student = await crud.get_student_by_roll_no(db, student.roll_no)
    if existing_student:
        raise HTTPException(status_code=400, detail="Student with this roll number already exists")
    
    return await crud.create_student(db, student=student)

@router.patch("/{student_id}", response_model=Student)
async def update_student(
    student_id: uuid.UUID, 
    student_update: StudentUpdate, 
    db: AsyncSession = Depends(get_database)
):
    """Update a student"""
    student = await crud.update_student(db, student_id=student_id, student_update=student_update)
    if student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    return student