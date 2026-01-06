from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker , DeclarativeBase
from sqlalchemy import create_engine
from app.core.config import settings

async_engine = create_async_engine(
    url = settings.DATABASE_URL_async,
    echo = True
    
)

async_session_factory = sessionmaker(
    bind = async_engine,
    class_ = AsyncSession,
    expire_on_commit= False,
)

sync_engine = create_engine(
    settings.DATABASE_URL_sync,
    echo=True
)

class Base(DeclarativeBase):
    pass

async def get_session():
    async with async_session_factory() as session:
        yield session
    