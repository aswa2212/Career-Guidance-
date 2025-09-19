from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base

from app.config import settings


# Create async engine with connection args to avoid URL encoding issues
if "postgresql" in settings.DATABASE_URL:
    # Use connection args for PostgreSQL to avoid password encoding issues
    engine = create_async_engine(
        "postgresql+asyncpg://postgres@localhost:5433/career_db",
        connect_args={"password": "Postgresql@0001"},
        future=True, 
        echo=True
    )
else:
    # Use regular URL for SQLite
    engine = create_async_engine(settings.DATABASE_URL, future=True, echo=True)

# Create async session
AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False
)

Base = declarative_base()


# Dependency to get DB session
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session


def get_database_url():
    """Get database URL for synchronous operations (like scraping)"""
    # Convert async URL to sync URL for SQLAlchemy sync operations
    url = settings.DATABASE_URL
    if url.startswith("postgresql+asyncpg://"):
        return url.replace("postgresql+asyncpg://", "postgresql://")
    return url