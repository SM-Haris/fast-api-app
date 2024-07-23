from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import declarative_base
from app.config import Config

async_engine = create_async_engine(url=Config.DATABASE_URL, echo=True)

Base = declarative_base()

async def init_db():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

session_maker = async_sessionmaker(async_engine, class_=AsyncSession, expire_on_commit=False)

async def get_session():
    async with session_maker() as session:
        yield session