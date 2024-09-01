from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy import select, desc, asc
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from app.application.models import Reserve, Product
from app.application.models.sale import Sale
from app.application.repositories import ProductRepository
from app.application.repositories.reserve import ReserveRepository
from app.core.constants import ErrorMessage, SortingOrder
from app.domain.dto.sale import SalesReportFilters


class SaleService:

    def __init__(self, session: AsyncSession):
        self.session = session
        self.product_repo = ProductRepository(session)
        self.reserve_repo = ReserveRepository(session)

    async def buy_product(self, product_id: int, user_id: UUID, quantity: int) -> Sale:
        product = await self.product_repo.get_product_by_id(product_id)

        if not product:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=ErrorMessage.PRODUCT_NOT_FOUND)
        reserve = (
            await self.session.execute(
                select(Reserve)
                .where(Reserve.user_id == user_id, Reserve.product_id == product_id)
            )
        ).scalar_one_or_none()

        if reserve:
            await self.reserve_repo.dereserve(reserve)
            product.stock_quantity += reserve.quantity

        if quantity > product.stock_quantity:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=ErrorMessage.OUT_OF_STOCK)

        sale = Sale(user_id=user_id, product_id=product.id, quantity=quantity)
        product.stock_quantity -= quantity
        self.session.add(sale)
        await self.session.commit()
        await self.session.refresh(sale, attribute_names=['id', 'product'])
        return sale

    async def get_sales_report(
        self,
        filters: SalesReportFilters,
        order_by: SortingOrder,
        offset: int,
        limit: int
    ) -> list[Sale]:
        query = select(Sale).join(Product).options(joinedload(Sale.product))

        if filters.start_date:
            query = query.where(Sale.created_at >= filters.start_date)

        if filters.end_date:
            query = query.where(Sale.created_at <= filters.end_date)

        if filters.min_price:
            query = query.where(Product.price >= filters.min_price)

        if filters.max_price:
            query = query.where(Product.price <= filters.max_price)

        if filters.category_ids:
            category_ids = filters.category_ids
            for category_id in filters.category_ids:
                subcategories = await self.product_repo.get_subcategories(category_id)
                category_ids.extend(subcategories)
            query = query.where(Product.category_id.in_(category_ids))

        if filters.product_ids:
            query = query.where(Sale.product_id.in_(filters.product_ids))

        if filters.user_ids:
            query = query.where(Sale.user_id.in_(filters.user_ids))

        if order_by:
            if order_by == SortingOrder.desc:
                query = query.order_by(desc(Sale.created_at))
            elif order_by == SortingOrder.asc:
                query = query.order_by(asc(Sale.created_at))


        query = query.offset(offset).limit(limit)

        results = await self.session.execute(query)
        sales = results.scalars().all()
        return sales
