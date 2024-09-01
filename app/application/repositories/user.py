from sqlalchemy import select

from app.domain.dto.user import UserCreate
from app.core.auth import generate_password_hash
from app.application.models import User


class UserRepository:

    def __init__(self, session):
        self.session = session

    async def create_user(self, user_create: UserCreate) -> User:
        hashed_password = generate_password_hash(user_create.password)
        user = User(username=user_create.username, hashed_password=hashed_password)
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return user

    async def get_user_by_username(self, username: str) -> User | None:
        user = (
            await self.session.execute(
                select(User)
                .where(User.username == username)
            )
        ).scalar_one_or_none()
        return user