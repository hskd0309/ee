from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime
from uuid import UUID
from models import AssignmentStatus, FeedbackSentiment, SessionStatus

# Student Schemas
class StudentBase(BaseModel):
    roll_no: str
    name: str
    email: EmailStr
    class_name: str
    department: str
    data_sharing: bool = True

class StudentCreate(StudentBase):
    pass

class StudentUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    class_name: Optional[str] = None
    department: Optional[str] = None
    data_sharing: Optional[bool] = None
    bri_score: Optional[int] = None
    attendance: Optional[int] = None
    avg_marks: Optional[float] = None
    gpa: Optional[float] = None

class Student(StudentBase):
    id: UUID
    bri_score: int
    attendance: int
    avg_marks: float
    gpa: float
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

# Assignment Schemas
class AssignmentBase(BaseModel):
    subject: str
    title: str
    due_date: datetime

class AssignmentCreate(AssignmentBase):
    student_id: UUID

class AssignmentUpdate(BaseModel):
    status: Optional[AssignmentStatus] = None
    submitted_at: Optional[datetime] = None
    grade: Optional[float] = None
    is_overdue: Optional[bool] = None

class Assignment(AssignmentBase):
    id: UUID
    student_id: UUID
    status: AssignmentStatus
    is_overdue: bool
    submitted_at: Optional[datetime] = None
    grade: Optional[float] = None
    created_at: datetime

    class Config:
        from_attributes = True

# Test Schemas
class TestBase(BaseModel):
    subject: str
    test_name: str
    date: datetime
    score: float
    total: float
    weightage: float = 1.0

class TestCreate(TestBase):
    student_id: UUID

class Test(TestBase):
    id: UUID
    student_id: UUID
    created_at: datetime

    class Config:
        from_attributes = True

# Feedback Schemas
class FeedbackBase(BaseModel):
    text: str
    category: Optional[str] = None

class FeedbackCreate(FeedbackBase):
    student_id: UUID

class Feedback(FeedbackBase):
    id: UUID
    student_id: UUID
    sentiment: FeedbackSentiment
    sentiment_score: float
    created_at: datetime

    class Config:
        from_attributes = True

# Counselling Session Schemas
class CounsellingSessionBase(BaseModel):
    counsellor_name: str
    session_date: datetime
    duration_minutes: int = 60
    referred_by: Optional[str] = None
    referred_date: Optional[datetime] = None

class CounsellingSessionCreate(CounsellingSessionBase):
    student_id: UUID

class CounsellingSessionUpdate(BaseModel):
    status: Optional[SessionStatus] = None
    notes: Optional[str] = None
    outcome: Optional[str] = None

class CounsellingSession(CounsellingSessionBase):
    id: UUID
    student_id: UUID
    status: SessionStatus
    notes: Optional[str] = None
    outcome: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True

# Dashboard Response Schemas
class StudentSummary(BaseModel):
    id: UUID
    name: str
    roll_no: str
    bri_score: int
    attendance: int
    avg_marks: float
    assignments_on_time: int
    sentiment: str
    data_sharing: bool
    bri_history: List[dict]
    attendance_data: List[dict]
    subject_marks: List[dict]

class ClassStats(BaseModel):
    class_name: str
    total_students: int
    high_risk_count: int
    medium_risk_count: int
    low_risk_count: int
    avg_bri_score: float
    avg_attendance: float

class MLPredictionRequest(BaseModel):
    attendance: float
    gpa: float
    sentiment_score: float

class MLPredictionResponse(BaseModel):
    risk_score: float
    risk_level: str
    color: str