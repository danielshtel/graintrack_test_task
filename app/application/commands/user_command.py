from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.application.dto.auth import AuthResponse
from app.application.dto.user import UserCreate, UserLogin
from app.application.services.auth import create_auth_response, verify_password
from app.application.services.user import UserService
from app.core.constants import ErrorMessage


class RegisterUserCommand:
    def __init__(self, user_create: UserCreate, session: AsyncSession):
        self.user_create = user_create
        self.session = session

    async def execute(self) -> AuthResponse:
        user_service = UserService(self.session)
        user = await user_service.create_user(self.user_create)
        auth_response = create_auth_response(user)
        return auth_response


class LoginUserCommand:
    def __init__(self, user_login: UserLogin, session: AsyncSession):
        self.user_login = user_login
        self.session = session

    async def execute(self) -> AuthResponse:
        user_service = UserService(self.session)
        user = await user_service.get_user_by_username(self.user_login.username)
        if user and verify_password(self.user_login.password, user.hashed_password):
            auth_response = create_auth_response(user)
            return auth_response
        else:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=ErrorMessage.INVALID_CREDENTIALS)
