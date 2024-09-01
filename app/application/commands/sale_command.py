from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.application.commands.base_command import BaseCommand
from app.application.services.sale import SaleService
from app.domain.dto import ProductOut
from app.domain.dto.sale import SaleIn, SaleOut, SalesReportFilters


class BuyProductCommand(BaseCommand):
    def __init__(self, sale_in: SaleIn, user_id: UUID, session: AsyncSession):
        self.session = session
        self.service = SaleService(session)
        self.sale_in = sale_in
        self.user_id = user_id

    async def execute(self) -> SaleOut:
        sale = await self.service.buy_product(self.sale_in.product_id, self.user_id, self.sale_in.quantity)
        sale_out = SaleOut(
            id=sale.id,
            quantity=sale.quantity,
            user_id=sale.user_id,
            created_at=sale.created_at,
            product=ProductOut(
                id=sale.product.id,
                name=sale.product.name,
                description=sale.product.description,
                price=sale.product.price,
                discount_percent=sale.product.discount_percent,
                stock_quantity=sale.product.stock_quantity,
                is_active=sale.product.is_active,
                is_discount=sale.product.is_discount,
                category_id=sale.product.category_id,
                discount_price=sale.product.discount_price,
            )
        )
        return sale_out


class SaleReportCommand(BaseCommand):

    def __init__(self, filters: SalesReportFilters, session: AsyncSession):
        self.filters = filters
        self.session = session
        self.sale_service = SaleService(session)

    async def execute(self) -> list[SaleOut]:
        sales = await self.sale_service.get_sales_report(
            filters=self.filters,
            order_by=self.filters.order_by,
            offset=self.filters.offset,
            limit=self.filters.limit
        )
        sales_out = [
            SaleOut(
                id=sale.id,
                quantity=sale.quantity,
                user_id=sale.user_id,
                created_at=sale.created_at,
                product=ProductOut(
                    id=sale.product.id,
                    name=sale.product.name,
                    description=sale.product.description,
                    price=sale.product.price,
                    discount_percent=sale.product.discount_percent,
                    stock_quantity=sale.product.stock_quantity,
                    is_active=sale.product.is_active,
                    is_discount=sale.product.is_discount,
                    category_id=sale.product.category_id,
                    discount_price=sale.product.discount_price,
                )
            )
            for sale in sales
        ]
        return sales_out
