import uuid

from sqlalchemy import UUID
from sqlalchemy.orm import mapped_column, Mapped

from app.infrastructure.database import ModelBase


class User(ModelBase):
    __tablename__ = 'users'

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        index=True,
        default=uuid.uuid4()
    )
    username: Mapped[str] = mapped_column(unique=True)
    hashed_password: Mapped[str] = mapped_column()
    is_admin: Mapped[bool] = mapped_column(default=False, server_default='0')