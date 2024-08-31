from sqlalchemy.ext.asyncio import AsyncSession

from app.application.dto.product import ProductIn, ProductUpdate
from app.domain.models import Product
from app.domain.repositories.product import ProductRepository


class ProductService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.product_repo = ProductRepository(session)

    async def create_product(self, product_in: ProductIn) -> Product:
        return await self.product_repo.create_product(product_in)


    async def get_product_by_id(self, product_id: int) -> Product:
        return await self.product_repo.get_product_by_id(product_id)


    async def update_product(self, product_update: ProductUpdate, product: Product) -> Product:
        return await self.product_repo.update_product(product_update, product)

    async def delete_product(self, product: Product) -> None:
        await self.product_repo.delete_product(product)

    async def filter_products(self, categories_ids: list[int]) -> list[Product]:
        return await self.product_repo.filter_products(categories_ids)


    async def list_products(self, offset: int, limit: int) -> list[Product]:
        return await self.product_repo.list_products(offset, limit)

