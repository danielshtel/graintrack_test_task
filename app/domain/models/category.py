from sqlalchemy import ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, relationship

from app.infrastructure.database import ModelBase


class Category(ModelBase):
    __tablename__ = 'categories'

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column()
    parent_category_id: Mapped[int | None] = mapped_column(ForeignKey('categories.id'), nullable=True)
