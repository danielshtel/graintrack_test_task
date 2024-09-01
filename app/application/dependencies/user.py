from uuid import UUID

from fastapi import HTTPException, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.application.dependencies.auth import verify_token
from app.application.dependencies.db import get_db_session
from app.core.constants import ErrorMessage
from app.application.models import User


async def get_user(token_claims: dict, session: AsyncSession) -> User:
    user_id = UUID(token_claims['sub'])
    user = await session.scalar(select(User).where(User.id == user_id))
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=ErrorMessage.USER_NOT_FOUND)
    return user


async def get_current_user(
    token_claims: dict = Depends(verify_token),
    session: AsyncSession = Depends(get_db_session)
) -> User:
    user = await get_user(token_claims, session)
    return user


async def get_current_admin(
    user: User = Depends(get_current_user),
) -> User:
    if not user.is_admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=ErrorMessage.NO_PERMISSIONS)
    return user

