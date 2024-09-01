import uuid

from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, relationship
from sqlalchemy.testing.schema import mapped_column

from app.infrastructure.database import ModelBase


class Reserve(ModelBase):
    __tablename__ = "reserves"

    __table_args__ = (
        UniqueConstraint('user_id', 'product_id', name='_user_product_uc'),
    )

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"))
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"))
    quantity: Mapped[int] = mapped_column()

    product: Mapped['Product'] = relationship()