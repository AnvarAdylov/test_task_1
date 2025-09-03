import os

from app.config import settings
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker

engine = create_async_engine(settings.DATABASE_URL, echo=True)


DATABASE_URL = os.getenv(
    "DATABASE_URL", "postgresql+psycopg2://postgres:postgres@db:5432/postgres"
)


async_session_maker = sessionmaker(
    bind=engine, class_=AsyncSession, expire_on_commit=False
)


Base = declarative_base()


async def get_db():
    async with async_session_maker() as session:
        yield session
