from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
import uuid

from database import get_database
from schemas import Test, TestCreate
import crud

router = APIRouter(prefix="/api/tests", tags=["tests"])

@router.get("/{student_id}", response_model=List[Test])
async def get_student_tests(student_id: uuid.UUID, db: AsyncSession = Depends(get_database)):
    """Get all tests for a specific student"""
    return await crud.get_tests_by_student(db, student_id=student_id)

@router.post("/", response_model=Test)
async def create_test(test: TestCreate, db: AsyncSession = Depends(get_database)):
    """Create a new test record"""
    return await crud.create_test(db, test=test)