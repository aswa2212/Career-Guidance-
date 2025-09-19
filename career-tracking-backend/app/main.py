from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db, engine
from app import models
from app.routers import auth, aptitude, suggestions, career, college, timeline, user, course, recommendations, courses, colleges

app = FastAPI(
    title="NEXTSTEP Career Guidance API",
    description="API for NEXTSTEP - comprehensive career guidance, aptitude testing, and educational recommendations",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origin_regex=r"http://(localhost|127\.0\.0\.1):\d+",  # Allow localhost and 127.0.0.1 on any port
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
app.include_router(courses.router)  # New courses router with real data
app.include_router(college.router)
app.include_router(colleges.router)  # New colleges router with real data
app.include_router(timeline.router)
app.include_router(user.router)
app.include_router(recommendations.router)

@app.get("/")
async def read_root():
    return {"message": "Welcome to the Personalized Career Tracking API"}

@app.get("/health")
async def health_check(db: AsyncSession = Depends(get_db)):
    # Simple health check that verifies DB connection
    return {"status": "ok", "db": "connected"}