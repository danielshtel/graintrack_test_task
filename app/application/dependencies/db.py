from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.database import AsyncSessionLocal


async def get_db_session() -> AsyncSession:
    async with AsyncSessionLocal() as db_session:
        yield db_session
