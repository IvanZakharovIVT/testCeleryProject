from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.ext.declarative import declarative_base

from config.settings import DATABASE_A_URL, DATABASE_URL

engine = create_async_engine(DATABASE_A_URL)
engine_sync = create_engine(DATABASE_URL)

AsyncSessionLocal = async_sessionmaker(bind=engine)

Base = declarative_base()

async def init_models():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def get_session():
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()
