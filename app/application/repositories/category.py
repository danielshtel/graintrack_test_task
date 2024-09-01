from sqlalchemy import select, desc
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.models import Category


class CategoryRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_category(self, name: str, parent_category_id: int | None) -> Category:
        category = Category(name=name, parent_category_id=parent_category_id)
        self.session.add(category)
        await self.session.commit()
        await self.session.refresh(category)
        return category

    async def get_category_by_id(self, category_id: int) -> Category:
        result = (
            await self.session.execute(
                select(Category)
                .where(Category.id == category_id)
            )
        )
        return result.scalar_one_or_none()

    async def list_categories(self, offset: int = 0, limit: int = 10) -> list[Category]:
        result = (
            await self.session.execute(
                select(Category)
                .offset(offset)
                .limit(limit)
                .order_by(desc(Category.created_at))
            )
        ).scalars().all()
        return result
