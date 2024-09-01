from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.commands.user_command import RegisterUserCommand, LoginUserCommand, GetNewTokenUserCommand
from app.application.dependencies.db import get_db_session
from app.application.dependencies.user import get_current_user
from app.application.models import User
from app.domain.dto.auth import AuthResponse
from app.domain.dto.user import UserCreate, UserLogin
from app.core.config import settings
from app.core.generics import ServiceResponse

router = APIRouter(prefix=settings.AUTH_API_PREFIX, tags=['Auth API'])


@router.post('/sign-up')
async def signup(
    user_create: UserCreate,
    session: AsyncSession = Depends(get_db_session)
) -> ServiceResponse[AuthResponse]:
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

@router.get('/token')
async def get_new_token_pair(
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db_session)
) -> ServiceResponse[AuthResponse]:
    get_new_token_command = GetNewTokenUserCommand(current_user, session)
    new_token = await get_new_token_command.execute()
    return ServiceResponse(data=new_token)