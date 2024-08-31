from sqlalchemy.ext.asyncio import AsyncSession

from app.application.dto.user import UserCreate
from app.domain.models.user import User
from app.domain.repositories.user import UserRepository


class UserService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.user_repo = UserRepository(session)

    async def create_user(self, user_create: UserCreate) -> User:
        return await self.user_repo.create_user(user_create)

    async def get_user_by_username(self, username: str) -> User:
        return await self.user_repo.get_user_by_username(username)