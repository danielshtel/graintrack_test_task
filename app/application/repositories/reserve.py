from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from app.application.models import Reserve, Product


class ReserveRepository:

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_reserve_by_id(self, reserve_id: int, user_id: UUID) -> Reserve | None:
        product = (
            await self.session.execute(
                select(Reserve)
                .where(Reserve.id == reserve_id, Reserve.user_id == user_id)
                .options(
                    joinedload(Reserve.product)
                )
            )
        ).scalar_one_or_none()
        return product

    async def reserve_product(self, product: Product, user_id: UUID, quantity: int) -> Reserve:
        reserve = Reserve(user_id=user_id, product_id=product.id, quantity=quantity)
        self.session.add(reserve)
        product.stock_quantity -= quantity
        await self.session.commit()
        await self.session.refresh(reserve, attribute_names=['id', 'product'])
        return reserve

    async def dereserve(self, reserve: Reserve, product: Product) -> None:
        product.stock_quantity += reserve.quantity
        await self.session.delete(reserve)
        await self.session.commit()

