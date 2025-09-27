from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from sqlalchemy import func, and_
from typing import List, Optional
import uuid
from datetime import datetime, timedelta
import random

from models import Student, Assignment, Test, Feedback, CounsellingSession
from schemas import (
    StudentCreate, StudentUpdate, AssignmentCreate, AssignmentUpdate,
    TestCreate, FeedbackCreate, CounsellingSessionCreate, CounsellingSessionUpdate
)

# Student CRUD
async def get_student(db: AsyncSession, student_id: uuid.UUID) -> Optional[Student]:
    result = await db.execute(
        select(Student).options(
            selectinload(Student.assignments),
            selectinload(Student.tests),
            selectinload(Student.feedback),
            selectinload(Student.counselling_sessions)
        ).where(Student.id == student_id)
    )
    return result.scalar_one_or_none()

async def get_student_by_roll_no(db: AsyncSession, roll_no: str) -> Optional[Student]:
    result = await db.execute(select(Student).where(Student.roll_no == roll_no))
    return result.scalar_one_or_none()

async def get_students(db: AsyncSession, skip: int = 0, limit: int = 100) -> List[Student]:
    result = await db.execute(select(Student).offset(skip).limit(limit))
    return result.scalars().all()

async def create_student(db: AsyncSession, student: StudentCreate) -> Student:
    db_student = Student(**student.dict())
    db.add(db_student)
    await db.commit()
    await db.refresh(db_student)
    return db_student

async def update_student(db: AsyncSession, student_id: uuid.UUID, student_update: StudentUpdate) -> Optional[Student]:
    result = await db.execute(select(Student).where(Student.id == student_id))
    db_student = result.scalar_one_or_none()
    if db_student:
        update_data = student_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_student, field, value)
        await db.commit()
        await db.refresh(db_student)
    return db_student

# Assignment CRUD
async def get_assignments_by_student(db: AsyncSession, student_id: uuid.UUID) -> List[Assignment]:
    result = await db.execute(select(Assignment).where(Assignment.student_id == student_id))
    return result.scalars().all()

async def create_assignment(db: AsyncSession, assignment: AssignmentCreate) -> Assignment:
    db_assignment = Assignment(**assignment.dict())
    db.add(db_assignment)
    await db.commit()
    await db.refresh(db_assignment)
    return db_assignment

# Test CRUD
async def get_tests_by_student(db: AsyncSession, student_id: uuid.UUID) -> List[Test]:
    result = await db.execute(select(Test).where(Test.student_id == student_id))
    return result.scalars().all()

async def create_test(db: AsyncSession, test: TestCreate) -> Test:
    db_test = Test(**test.dict())
    db.add(db_test)
    await db.commit()
    await db.refresh(db_test)
    return db_test

# Feedback CRUD
async def get_feedback_by_student(db: AsyncSession, student_id: uuid.UUID) -> List[Feedback]:
    result = await db.execute(select(Feedback).where(Feedback.student_id == student_id))
    return result.scalars().all()

async def create_feedback(db: AsyncSession, feedback: FeedbackCreate) -> Feedback:
    # Simple sentiment analysis (would use a real ML model in production)
    sentiment_score = random.uniform(-1, 1)  # Placeholder
    sentiment = "positive" if sentiment_score > 0.2 else "negative" if sentiment_score < -0.2 else "neutral"
    
    db_feedback = Feedback(
        **feedback.dict(),
        sentiment=sentiment,
        sentiment_score=sentiment_score
    )
    db.add(db_feedback)
    await db.commit()
    await db.refresh(db_feedback)
    return db_feedback

# Counselling Session CRUD
async def get_counselling_sessions_by_student(db: AsyncSession, student_id: uuid.UUID) -> List[CounsellingSession]:
    result = await db.execute(select(CounsellingSession).where(CounsellingSession.student_id == student_id))
    return result.scalars().all()

async def create_counselling_session(db: AsyncSession, session: CounsellingSessionCreate) -> CounsellingSession:
    db_session = CounsellingSession(**session.dict())
    db.add(db_session)
    await db.commit()
    await db.refresh(db_session)
    return db_session

async def update_counselling_session(db: AsyncSession, session_id: uuid.UUID, session_update: CounsellingSessionUpdate) -> Optional[CounsellingSession]:
    result = await db.execute(select(CounsellingSession).where(CounsellingSession.id == session_id))
    db_session = result.scalar_one_or_none()
    if db_session:
        update_data = session_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_session, field, value)
        await db.commit()
        await db.refresh(db_session)
    return db_session

# Analytics functions
async def get_class_stats(db: AsyncSession, class_name: str) -> dict:
    # Get students in the class
    result = await db.execute(select(Student).where(Student.class_name == class_name))
    students = result.scalars().all()
    
    if not students:
        return {"error": "Class not found"}
    
    total_students = len(students)
    high_risk = sum(1 for s in students if s.bri_score < 40)
    medium_risk = sum(1 for s in students if 40 <= s.bri_score < 70)
    low_risk = sum(1 for s in students if s.bri_score >= 70)
    avg_bri = sum(s.bri_score for s in students) / total_students
    avg_attendance = sum(s.attendance for s in students) / total_students
    
    return {
        "class_name": class_name,
        "total_students": total_students,
        "high_risk_count": high_risk,
        "medium_risk_count": medium_risk,
        "low_risk_count": low_risk,
        "avg_bri_score": round(avg_bri, 2),
        "avg_attendance": round(avg_attendance, 2)
    }

async def get_student_summary(db: AsyncSession, student_id: uuid.UUID) -> dict:
    student = await get_student(db, student_id)
    if not student:
        return {"error": "Student not found"}
    
    # Calculate assignments on time percentage
    total_assignments = len(student.assignments)
    on_time_assignments = sum(1 for a in student.assignments if not a.is_overdue and a.status.value == "completed")
    assignments_on_time = round((on_time_assignments / total_assignments * 100) if total_assignments > 0 else 100)
    
    # Generate mock BRI history (would come from historical data)
    bri_history = [
        {"month": "Jan", "score": student.bri_score + random.randint(-5, 5)},
        {"month": "Feb", "score": student.bri_score + random.randint(-5, 5)},
        {"month": "Mar", "score": student.bri_score + random.randint(-5, 5)},
        {"month": "Apr", "score": student.bri_score + random.randint(-5, 5)},
        {"month": "May", "score": student.bri_score + random.randint(-5, 5)},
        {"month": "Jun", "score": student.bri_score}
    ]
    
    # Generate attendance data
    attendance_data = [
        {"name": "Present", "value": student.attendance, "fill": "#22c55e"},
        {"name": "Absent", "value": 100 - student.attendance, "fill": "#ef4444"}
    ]
    
    # Generate subject marks from tests
    subject_marks = []
    subjects = list(set([test.subject for test in student.tests]))
    for subject in subjects:
        subject_tests = [test for test in student.tests if test.subject == subject]
        avg_score = sum(test.score for test in subject_tests) / len(subject_tests) if subject_tests else 0
        subject_marks.append({"subject": subject, "marks": round(avg_score)})
    
    sentiment = "positive" if len([f for f in student.feedback if f.sentiment.value == "positive"]) > len([f for f in student.feedback if f.sentiment.value == "negative"]) else "neutral"
    
    return {
        "id": student.id,
        "name": student.name,
        "roll_no": student.roll_no,
        "bri_score": student.bri_score,
        "attendance": student.attendance,
        "avg_marks": student.avg_marks,
        "assignments_on_time": assignments_on_time,
        "sentiment": sentiment,
        "data_sharing": student.data_sharing,
        "bri_history": bri_history,
        "attendance_data": attendance_data,
        "subject_marks": subject_marks
    }