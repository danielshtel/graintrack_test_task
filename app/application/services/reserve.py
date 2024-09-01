from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.models import Reserve
from app.application.repositories import ProductRepository
from app.application.repositories.reserve import ReserveRepository
from app.core.constants import ErrorMessage


class ReserveService:

    def __init__(self, session: AsyncSession):
        self.session = session
        self.product_repo = ProductRepository(session)
        self.reserve_repo = ReserveRepository(session
                                              )
    async def reserve_product(self, product_id: int, user_id: UUID, quantity: int) -> Reserve:
        product = await self.product_repo.get_product_by_id(product_id)

        if not product:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=ErrorMessage.PRODUCT_NOT_FOUND)

        if quantity > product.stock_quantity:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=ErrorMessage.OUT_OF_STOCK)

        try:
            reserve = await self.reserve_repo.reserve_product(product, user_id, quantity)
        except IntegrityError:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=ErrorMessage.ALREADY_RESERVED)

        return reserve

    async def dereserve_product(self, reserve_id: int, user_id: UUID) -> bool:

        reserve = await self.reserve_repo.get_reserve_by_id(reserve_id, user_id)

        if not reserve:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=ErrorMessage.RESERVE_NOT_FOUND)

        product = await self.product_repo.get_product_by_id(reserve.product_id)

        if not product:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=ErrorMessage.PRODUCT_NOT_FOUND)

        await self.reserve_repo.dereserve(reserve, product)

        return True