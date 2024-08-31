from sqlalchemy.ext.asyncio import AsyncSession

from app.application.dto.category import CategoryIn
from app.domain.models import Category
from app.domain.repositories.category import CategoryRepository


class CategoryService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.category_repo = CategoryRepository(session)

    async def create_category(self, category_in: CategoryIn) -> Category:
        return await self.category_repo.create_category(category_in.name, category_in.parent_category_id)

    async def get_category_by_id(self, category_id: int) -> Category:
        return await self.category_repo.get_category_by_id(category_id)

    async def list_categories(self, offset: int = 0, limit: int = 10):
        return await self.category_repo.list_categories(offset, limit)
