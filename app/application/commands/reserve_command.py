from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.application.commands.base_command import BaseCommand
from app.application.services.reserve import ReserveService
from app.domain.dto import ProductOut
from app.domain.dto.reserve import ReserveOut, ReserveIn


class ReserveBaseCommand(BaseCommand):
    def __init__(self, session: AsyncSession):
        self.service = ReserveService(session)


class ReserveProductCommand(ReserveBaseCommand):

    def __init__(self, reserve_in: ReserveIn, user_id: UUID, session: AsyncSession):
        super().__init__(session)
        self.product_id = reserve_in.product_id
        self.user_id = user_id
        self.quantity = reserve_in.quantity

    async def execute(self) -> ReserveOut:
        reserve = await self.service.reserve_product(self.product_id, self.user_id, self.quantity)

        reserve_out = ReserveOut(
            id=reserve.id,
            quantity=reserve.quantity,
            user_id=reserve.user_id,
            product=ProductOut(
                id=reserve.product.id,
                name=reserve.product.name,
                description=reserve.product.description,
                price=reserve.product.price,
                discount_percent=reserve.product.discount_percent,
                stock_quantity=reserve.product.stock_quantity,
                is_active=reserve.product.is_active,
                is_discount=reserve.product.is_discount,
                category_id=reserve.product.category_id,
                discount_price=reserve.product.discount_price
            )
        )
        return reserve_out


class CancelReserveProductCommand(ReserveBaseCommand):

    def __init__(self, user_id: UUID, reserve_id: int, session: AsyncSession):
        super().__init__(session)
        self.user_id = user_id
        self.reserve_id = reserve_id

    async def execute(self) -> bool:
        result = await self.service.dereserve_product(self.reserve_id, self.user_id)
        return result
