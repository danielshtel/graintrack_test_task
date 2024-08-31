from decimal import Decimal

from sqlalchemy import Numeric, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.infrastructure.database import ModelBase


class Product(ModelBase):
    __tablename__ = 'products'

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column()
    description: Mapped[str] = mapped_column()
    price: Mapped[Decimal] = mapped_column(Numeric(precision=10, scale=2))
    discount_percent: Mapped[Decimal | None] = mapped_column(Numeric(precision=10, scale=2), nullable=True)
    stock_quantity: Mapped[int] = mapped_column(default=0, server_default='0')
    reserved_quantity: Mapped[int] = mapped_column(default=0, server_default='0')
    is_active: Mapped[bool] = mapped_column(default=True, server_default='1')
    is_discount: Mapped[bool] = mapped_column(default=False, server_default='0')

    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id"), nullable=False)