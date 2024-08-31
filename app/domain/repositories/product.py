from sqlalchemy import select, desc
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.dto.product import ProductIn, ProductUpdate
from app.domain.models import Product, Category


class ProductRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_product(self, product_in: ProductIn) -> Product:
        product = Product(
            name=product_in.name,
            description=product_in.description,
            price=product_in.price,
            stock_quantity=product_in.stock_quantity,
            category_id=product_in.category_id
        )
        self.session.add(product)
        await self.session.commit()
        await self.session.refresh(product)
        return product

    async def get_product_by_id(self, product_id: int) -> Product | None:
        product = (
            await self.session.execute(
                select(Product)
                .where(Product.id == product_id)
            )
        ).scalar_one_or_none()
        return product

    async def update_product(self, product_update: ProductUpdate, product: Product) -> Product:
        product.name = product_update.name
        product.description = product_update.description
        product.price = product_update.price
        product.discount_percent = product_update.discount_percent
        product.stock_quantity = product_update.stock_quantity
        product.is_active = product_update.is_active
        product.is_discount = product_update.is_discount
        product.category_id = product_update.category_id
        await self.session.merge(product)
        await self.session.commit()
        await self.session.refresh(product)
        return product

    async def delete_product(self, product: Product) -> None:
        await self.session.delete(product)
        await self.session.commit()

    async def get_subcategories(self, category_id: int) -> list[int]:
        subcategory_ids = (
            await self.session.execute(
                select(Category.id)
                .where(Category.parent_category_id == category_id)
            )
        ).scalars().all()

        return subcategory_ids

    async def filter_products(self, category_ids) -> list[Product]:
        for category_id in category_ids:
            subcategories = await self.get_subcategories(category_id)
            category_ids.extend(subcategories)

        products = (
            await self.session.execute(
                select(Product)
                .where(
                    Product.category_id.in_(category_ids),
                    Product.stock_quantity > 0
                )
            )
        ).scalars().all()

        return products

    async def list_products(self, offset, limit):
        products = (
            await self.session.execute(
                select(Product)
                .where(Product.stock_quantity > 0)
                .offset(offset)
                .limit(limit)
                .order_by(desc(Product.created_at))
            )
        ).scalars().all()
        return products
