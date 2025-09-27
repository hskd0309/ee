import asyncio
import random
from datetime import datetime, timedelta
from uuid import uuid4

from database import AsyncSessionLocal, engine
from models import Base, Student, Assignment, Test, Feedback, CounsellingSession, AssignmentStatus, FeedbackSentiment, SessionStatus

async def create_tables():
    """Create all database tables"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    print("Database tables created!")

async def seed_database():
    """Seed the database with sample data"""
    async with AsyncSessionLocal() as db:
        # Sample student data
        students_data = [
            {"roll_no": "CSE001", "name": "Arjun Sharma", "email": "arjun.sharma@college.edu", "class_name": "CSE-A", "department": "Computer Science"},
            {"roll_no": "CSE002", "name": "Priya Patel", "email": "priya.patel@college.edu", "class_name": "CSE-A", "department": "Computer Science"},
            {"roll_no": "CSE003", "name": "Rahul Kumar", "email": "rahul.kumar@college.edu", "class_name": "CSE-B", "department": "Computer Science"},
            {"roll_no": "CSE004", "name": "Sneha Singh", "email": "sneha.singh@college.edu", "class_name": "CSE-B", "department": "Computer Science"},
            {"roll_no": "CSE005", "name": "Amit Gupta", "email": "amit.gupta@college.edu", "class_name": "CSE-A", "department": "Computer Science"},
            {"roll_no": "ECE001", "name": "Neha Reddy", "email": "neha.reddy@college.edu", "class_name": "ECE-A", "department": "Electronics"},
            {"roll_no": "ECE002", "name": "Vikram Rao", "email": "vikram.rao@college.edu", "class_name": "ECE-A", "department": "Electronics"},
            {"roll_no": "MECH001", "name": "Kiran Shah", "email": "kiran.shah@college.edu", "class_name": "MECH-A", "department": "Mechanical"},
            {"roll_no": "MECH002", "name": "Pooja Joshi", "email": "pooja.joshi@college.edu", "class_name": "MECH-A", "department": "Mechanical"},
            {"roll_no": "CSE006", "name": "Rohit Verma", "email": "rohit.verma@college.edu", "class_name": "CSE-B", "department": "Computer Science"},
            {"roll_no": "CSE007", "name": "Anita Das", "email": "anita.das@college.edu", "class_name": "CSE-A", "department": "Computer Science"},
            {"roll_no": "EEE001", "name": "Suresh Nair", "email": "suresh.nair@college.edu", "class_name": "EEE-A", "department": "Electrical"},
        ]
        
        created_students = []
        for student_data in students_data:
            # Generate realistic metrics
            bri_score = random.randint(30, 90)
            attendance = random.randint(60, 95)
            avg_marks = random.uniform(60.0, 90.0)
            gpa = random.uniform(2.5, 4.0)
            
            student = Student(
                **student_data,
                bri_score=bri_score,
                attendance=attendance,
                avg_marks=round(avg_marks, 2),
                gpa=round(gpa, 2),
                data_sharing=random.choice([True, True, True, False])  # Most students share data
            )
            db.add(student)
            created_students.append(student)
        
        await db.commit()
        print(f"Created {len(created_students)} students")
        
        # Refresh to get IDs
        for student in created_students:
            await db.refresh(student)
        
        # Create assignments
        subjects = ["Mathematics", "Physics", "Chemistry", "Computer Science", "English", "Data Structures", "Algorithms", "Database Systems"]
        assignment_titles = [
            "Linear Algebra Problems", "Calculus Assignment", "Physics Lab Report", 
            "Chemistry Experiment", "Essay Writing", "Programming Assignment",
            "Data Structure Implementation", "Algorithm Analysis", "Database Design Project"
        ]
        
        assignments_created = 0
        for student in created_students:
            # Create 3-5 assignments per student
            num_assignments = random.randint(3, 5)
            for _ in range(num_assignments):
                assignment = Assignment(
                    student_id=student.id,
                    subject=random.choice(subjects),
                    title=random.choice(assignment_titles),
                    due_date=datetime.now() + timedelta(days=random.randint(-30, 30)),
                    status=random.choice([AssignmentStatus.pending, AssignmentStatus.completed]),
                    is_overdue=random.choice([True, False]) if random.random() < 0.2 else False,
                    submitted_at=datetime.now() - timedelta(days=random.randint(1, 10)) if random.random() < 0.7 else None,
                    grade=random.uniform(60, 95) if random.random() < 0.6 else None
                )
                db.add(assignment)
                assignments_created += 1
        
        await db.commit()
        print(f"Created {assignments_created} assignments")
        
        # Create test records
        test_names = [
            "Midterm Exam", "Final Exam", "Quiz 1", "Quiz 2", "Unit Test",
            "Programming Test", "Lab Practical", "Viva Voce"
        ]
        
        tests_created = 0
        for student in created_students:
            # Create 4-8 tests per student
            num_tests = random.randint(4, 8)
            for _ in range(num_tests):
                total_marks = random.choice([50, 100, 25, 30])
                score = random.uniform(0.6 * total_marks, 0.95 * total_marks)
                
                test = Test(
                    student_id=student.id,
                    subject=random.choice(subjects),
                    test_name=random.choice(test_names),
                    date=datetime.now() - timedelta(days=random.randint(1, 90)),
                    score=round(score, 2),
                    total=total_marks,
                    weightage=random.choice([0.5, 1.0, 1.5, 2.0])
                )
                db.add(test)
                tests_created += 1
        
        await db.commit()
        print(f"Created {tests_created} test records")
        
        # Create feedback
        feedback_texts = [
            "I'm feeling overwhelmed with the coursework this semester.",
            "The professors are very helpful and supportive.",
            "I'm struggling to keep up with assignments.",
            "Really enjoying the practical sessions.",
            "The workload is manageable and I'm learning a lot.",
            "I feel stressed about upcoming exams.",
            "Great learning environment and resources.",
            "Need more time for understanding complex topics.",
            "Happy with my academic progress so far.",
            "Sometimes feel isolated from classmates."
        ]
        
        feedback_created = 0
        for student in created_students:
            # Create 1-3 feedback entries per student
            num_feedback = random.randint(1, 3)
            for _ in range(num_feedback):
                text = random.choice(feedback_texts)
                sentiment = random.choice([FeedbackSentiment.positive, FeedbackSentiment.neutral, FeedbackSentiment.negative])
                sentiment_score = random.uniform(-1, 1)
                
                feedback = Feedback(
                    student_id=student.id,
                    text=text,
                    category=random.choice(["Academic", "Personal", "Social", "Health"]),
                    sentiment=sentiment,
                    sentiment_score=sentiment_score
                )
                db.add(feedback)
                feedback_created += 1
        
        await db.commit()
        print(f"Created {feedback_created} feedback entries")
        
        # Create counselling sessions
        counsellors = ["Dr. Sarah Wilson", "Prof. Michael Brown", "Dr. Priya Mehta", "Dr. James Anderson"]
        
        sessions_created = 0
        # Create sessions for students with lower BRI scores (higher risk)
        high_risk_students = [s for s in created_students if s.bri_score < 60]
        
        for student in high_risk_students:
            if random.random() < 0.7:  # 70% chance of having a session
                session = CounsellingSession(
                    student_id=student.id,
                    counsellor_name=random.choice(counsellors),
                    referred_by="Academic Advisor" if random.random() < 0.6 else "Self-referred",
                    referred_date=datetime.now() - timedelta(days=random.randint(5, 30)),
                    session_date=datetime.now() - timedelta(days=random.randint(1, 15)),
                    duration_minutes=random.choice([45, 60, 90]),
                    status=random.choice([SessionStatus.active, SessionStatus.in_progress, SessionStatus.closed]),
                    notes="Student discussing academic stress and time management strategies.",
                    outcome="Follow-up session scheduled" if random.random() < 0.5 else "Referred to academic support services"
                )
                db.add(session)
                sessions_created += 1
        
        await db.commit()
        print(f"Created {sessions_created} counselling sessions")
        
        print("Database seeding completed successfully!")

async def main():
    """Main function to set up and seed the database"""
    print("Setting up database...")
    await create_tables()
    await seed_database()
    print("All done!")

if __name__ == "__main__":
    asyncio.run(main())