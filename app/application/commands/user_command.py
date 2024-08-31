from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.application.commands.base_command import BaseCommand
from app.application.dto.auth import AuthResponse
from app.application.dto.user import UserCreate, UserLogin
from app.application.services.auth import create_auth_response, verify_password
from app.application.services.user import UserService
from app.core.constants import ErrorMessage


class BaseUserCommand(BaseCommand):
    def __init__(self, session: AsyncSession):
        self.session = session


class RegisterUserCommand(BaseUserCommand):
    def __init__(self, user_create: UserCreate, session: AsyncSession):
        super().__init__(session)
        self.user_create = user_create

    async def execute(self) -> AuthResponse:
        user_service = UserService(self.session)
        user = await user_service.get_user_by_username(self.user_create.username)
        if user:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=ErrorMessage.USER_IS_ALREADY_REGISTERED)
        user = await user_service.create_user(self.user_create)
        auth_response = create_auth_response(user)
        return auth_response


class LoginUserCommand(BaseUserCommand):
    def __init__(self, user_login: UserLogin, session: AsyncSession):
        super().__init__(session)
        self.user_login = user_login

    async def execute(self) -> AuthResponse:
        user_service = UserService(self.session)
        user = await user_service.get_user_by_username(self.user_login.username)
        if user and verify_password(self.user_login.password, user.hashed_password):
            auth_response = create_auth_response(user)
            return auth_response
        else:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=ErrorMessage.INVALID_CREDENTIALS)
