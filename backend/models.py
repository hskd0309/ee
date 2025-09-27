from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text, Float, ForeignKey, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid
import enum
from database import Base

class AssignmentStatus(enum.Enum):
    pending = "pending"
    completed = "completed"

class FeedbackSentiment(enum.Enum):
    positive = "positive"
    neutral = "neutral"
    negative = "negative"

class SessionStatus(enum.Enum):
    active = "active"
    in_progress = "in_progress"
    closed = "closed"

class Student(Base):
    __tablename__ = "students"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    roll_no = Column(String(20), unique=True, nullable=False, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    class_name = Column(String(50), nullable=False)
    department = Column(String(50), nullable=False)
    data_sharing = Column(Boolean, default=True)
    bri_score = Column(Integer, default=70)
    attendance = Column(Integer, default=85)
    avg_marks = Column(Float, default=75.0)
    gpa = Column(Float, default=3.0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    assignments = relationship("Assignment", back_populates="student")
    tests = relationship("Test", back_populates="student")
    feedback = relationship("Feedback", back_populates="student")
    counselling_sessions = relationship("CounsellingSession", back_populates="student")

class Assignment(Base):
    __tablename__ = "assignments"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    student_id = Column(UUID(as_uuid=True), ForeignKey("students.id"), nullable=False)
    subject = Column(String(100), nullable=False)
    title = Column(String(200), nullable=False)
    due_date = Column(DateTime, nullable=False)
    status = Column(Enum(AssignmentStatus), default=AssignmentStatus.pending)
    is_overdue = Column(Boolean, default=False)
    submitted_at = Column(DateTime, nullable=True)
    grade = Column(Float, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    student = relationship("Student", back_populates="assignments")

class Test(Base):
    __tablename__ = "tests"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    student_id = Column(UUID(as_uuid=True), ForeignKey("students.id"), nullable=False)
    subject = Column(String(100), nullable=False)
    test_name = Column(String(200), nullable=False)
    date = Column(DateTime, nullable=False)
    score = Column(Float, nullable=False)
    total = Column(Float, nullable=False)
    weightage = Column(Float, default=1.0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    student = relationship("Student", back_populates="tests")

class Feedback(Base):
    __tablename__ = "feedback"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    student_id = Column(UUID(as_uuid=True), ForeignKey("students.id"), nullable=False)
    text = Column(Text, nullable=False)
    category = Column(String(100), nullable=True)
    sentiment = Column(Enum(FeedbackSentiment), default=FeedbackSentiment.neutral)
    sentiment_score = Column(Float, default=0.0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    student = relationship("Student", back_populates="feedback")

class CounsellingSession(Base):
    __tablename__ = "counselling_sessions"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    student_id = Column(UUID(as_uuid=True), ForeignKey("students.id"), nullable=False)
    counsellor_name = Column(String(100), nullable=False)
    referred_by = Column(String(100), nullable=True)
    referred_date = Column(DateTime, nullable=True)
    session_date = Column(DateTime, nullable=False)
    duration_minutes = Column(Integer, default=60)
    status = Column(Enum(SessionStatus), default=SessionStatus.active)
    notes = Column(Text, nullable=True)
    outcome = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    student = relationship("Student", back_populates="counselling_sessions")