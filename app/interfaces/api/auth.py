from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.commands.user_command import RegisterUserCommand, LoginUserCommand
from app.application.dependencies.db import get_db_session
from app.application.dto.auth import AuthResponse
from app.application.dto.user import UserCreate, UserLogin
from app.core.config import settings
from app.core.generics import ServiceResponse

router = APIRouter(prefix=settings.AUTH_PREFIX, tags=['Auth API'])


@router.post('/sign-up')
async def signup(
    user_create: UserCreate,
    session: AsyncSession = Depends(get_db_session)
) -> ServiceResponse[AuthResponse]:
    # TODO: add try/except
    register_command = RegisterUserCommand(user_create, session)
    auth_response = await register_command.execute()
    return ServiceResponse(data=auth_response)


@router.post('/sign-in')
async def sign_in(
    user_login: UserLogin,
    session: AsyncSession = Depends(get_db_session)
) -> ServiceResponse[AuthResponse]:
    login_command = LoginUserCommand(user_login, session)
    auth_response = await login_command.execute()
    return ServiceResponse(data=auth_response)
