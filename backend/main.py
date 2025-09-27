from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import os
from dotenv import load_dotenv

# Import routers
from routers import students, assignments, tests, feedback, counselling, ml
from database import engine
from models import Base

# Load environment variables
load_dotenv()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    print("Starting up Smart Campus ERP API...")
    # Create database tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("Database tables created successfully!")
    yield
    # Shutdown
    print("Shutting down Smart Campus ERP API...")

app = FastAPI(
    title="Smart Campus ERP API",
    description="Backend API for Student Wellness Monitoring System",
    version="1.0.0",
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5000", "http://127.0.0.1:5000", "*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(students.router)
app.include_router(assignments.router)
app.include_router(tests.router)
app.include_router(feedback.router)
app.include_router(counselling.router)
app.include_router(ml.router)

@app.get("/")
async def root():
    return {"message": "Smart Campus ERP API is running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "Smart Campus ERP API"}

@app.get("/api/classes/{class_name}/stats")
async def get_class_stats(class_name: str):
    """Get class statistics"""
    from database import AsyncSessionLocal
    import crud
    
    async with AsyncSessionLocal() as db:
        stats = await crud.get_class_stats(db, class_name)
        return stats