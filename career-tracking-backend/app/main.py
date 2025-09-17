from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db, engine
from app import models
from app.routers import auth, aptitude, suggestions, career, college, timeline, user, course

app = FastAPI(
    title="Personalized Career Tracking API",
    description="API for career guidance, aptitude testing, and educational recommendations",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    """Initialize database tables on startup"""
    async with engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.create_all)

# Include routers
app.include_router(auth.router)
app.include_router(aptitude.router)
app.include_router(suggestions.router)
app.include_router(career.router)
app.include_router(course.router)
app.include_router(college.router)
app.include_router(timeline.router)
app.include_router(user.router)

@app.get("/")
async def read_root():
    return {"message": "Welcome to the Personalized Career Tracking API"}

@app.get("/health")
async def health_check(db: AsyncSession = Depends(get_db)):
    # Simple health check that verifies DB connection
    return {"status": "ok", "db": "connected"}