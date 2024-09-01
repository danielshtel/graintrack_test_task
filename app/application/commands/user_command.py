from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.application.commands.base_command import BaseCommand
from app.application.repositories import UserRepository
from app.core.auth import create_auth_response, verify_password
from app.core.constants import ErrorMessage
from app.domain.dto.auth import AuthResponse
from app.domain.dto.user import UserCreate, UserLogin


class BaseUserCommand(BaseCommand):
    def __init__(self, session: AsyncSession):
        self.session = session
        self.repo = UserRepository(self.session)

class RegisterUserCommand(BaseUserCommand):
    def __init__(self, user_create: UserCreate, session: AsyncSession):
        super().__init__(session)
        self.user_create = user_create

    async def execute(self) -> AuthResponse:

        user = await self.repo.get_user_by_username(self.user_create.username)
        if user:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=ErrorMessage.USER_IS_ALREADY_REGISTERED)
        user = await self.repo.create_user(self.user_create)
        auth_response = create_auth_response(user)
        return auth_response


class LoginUserCommand(BaseUserCommand):
    def __init__(self, user_login: UserLogin, session: AsyncSession):
        super().__init__(session)
        self.user_login = user_login

    async def execute(self) -> AuthResponse:
        user = await self.repo.get_user_by_username(self.user_login.username)
        if user and verify_password(self.user_login.password, user.hashed_password):
            auth_response = create_auth_response(user)
            return auth_response
        else:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=ErrorMessage.INVALID_CREDENTIALS)
