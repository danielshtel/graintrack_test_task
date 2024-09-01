from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.commands.base_command import BaseCommand
from app.application.repositories import ProductRepository
from app.core.constants import ErrorMessage
from app.domain.dto.product import ProductIn, ProductOut, ProductUpdate


class BaseProductCommand(BaseCommand):
    def __init__(self, session: AsyncSession):
        self.session = session
        self.repo = ProductRepository(session)


class CreateProductCommand(BaseProductCommand):
    def __init__(self, product_in: ProductIn, session: AsyncSession):
        super().__init__(session)
        self.product_in = product_in

    async def execute(self) -> ProductOut:
        product = await self.repo.create_product(self.product_in)
        product_out = ProductOut(
            id=product.id,
            name=product.name,
            description=product.description,
            price=product.price,
            discount_percent=product.discount_percent,
            stock_quantity=product.stock_quantity,
            is_active=product.is_active,
            is_discount=product.is_discount,
            category_id=product.category_id,
            discount_price=product.discount_price
        )
        return product_out


class UpdateProductCommand(BaseProductCommand):
    def __init__(self, product_id, product_update: ProductUpdate, session: AsyncSession):
        super().__init__(session)
        self.product_id = product_id
        self.product_update = product_update

    async def execute(self) -> ProductOut:
        product = await self.repo.get_product_by_id(self.product_id)

        if not product:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=ErrorMessage.PRODUCT_NOT_FOUND)

        product = await self.repo.update_product(self.product_update, product)
        product_out = ProductOut(
            id=product.id,
            name=product.name,
            description=product.description,
            price=product.price,
            discount_percent=product.discount_percent,
            stock_quantity=product.stock_quantity,
            is_active=product.is_active,
            is_discount=product.is_discount,
            category_id=product.category_id,
            discount_price=product.discount_price
        )
        return product_out


class DeleteProductCommand(BaseProductCommand):
    def __init__(self, product_id, session: AsyncSession):
        super().__init__(session)
        self.product_id = product_id

    async def execute(self) -> None:
        product = await self.repo.get_product_by_id(self.product_id)

        if not product:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=ErrorMessage.PRODUCT_NOT_FOUND)

        await self.repo.delete_product(product)


class FilterProductCommand(BaseProductCommand):
    def __init__(self, categories_ids: list[int], offset: int, limit: int, session: AsyncSession):
        super().__init__(session)
        self.categories_ids = categories_ids
        self.offset = offset
        self.limit = limit

    async def execute(self) -> list[ProductOut]:
        products = await self.repo.filter_products(self.categories_ids, self.offset, self.limit)
        products_out = [
            ProductOut(
                id=product.id,
                name=product.name,
                description=product.description,
                price=product.price,
                discount_percent=product.discount_percent,
                stock_quantity=product.stock_quantity,
                is_active=product.is_active,
                is_discount=product.is_discount,
                category_id=product.category_id,
                discount_price=product.discount_price
            )
            for product in products
        ]
        return products_out


class GetProductCommand(BaseProductCommand):
    def __init__(self, product_id, session: AsyncSession):
        super().__init__(session)
        self.product_id = product_id

    async def execute(self) -> ProductOut:
        product = await self.repo.get_product_by_id(self.product_id)

        if not product:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=ErrorMessage.PRODUCT_NOT_FOUND)

        product_out = ProductOut(
            id=product.id,
            name=product.name,
            description=product.description,
            price=product.price,
            discount_percent=product.discount_percent,
            stock_quantity=product.stock_quantity,
            is_active=product.is_active,
            is_discount=product.is_discount,
            category_id=product.category_id,
            discount_price=product.discount_price
        )
        return product_out


class ListProductCommand(BaseProductCommand):
    def __init__(self, offset: int, limit: int, session: AsyncSession):
        super().__init__(session)
        self.offset = offset
        self.limit = limit

    async def execute(self) -> list[ProductOut]:
        products = await self.repo.list_products(self.offset, self.limit)
        products_out = [
            ProductOut(
                id=product.id,
                name=product.name,
                description=product.description,
                price=product.price,
                discount_percent=product.discount_percent,
                stock_quantity=product.stock_quantity,
                is_active=product.is_active,
                is_discount=product.is_discount,
                category_id=product.category_id,
                discount_price=product.discount_price
            )
            for product in products
        ]
        return products_out
