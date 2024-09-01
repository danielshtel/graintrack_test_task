from fastapi import status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.commands.base_command import BaseCommand
from app.application.repositories import CategoryRepository
from app.core.constants import ErrorMessage
from app.domain.dto import CategoryOut, CategoryIn


class BaseCategoryCommand(BaseCommand):
    def __init__(self, session: AsyncSession):
        self.session = session
        self.repo = CategoryRepository(session)


class CreateCategoryCommand(BaseCategoryCommand):

    def __init__(self, category_in: CategoryIn, session: AsyncSession):
        super().__init__(session)
        self.category_in = category_in

    async def execute(self) -> CategoryOut:
        category = await self.repo.create_category(self.category_in.name, self.category_in.parent_category_id)
        category_out = CategoryOut(id=category.id, name=category.name, parent_category_id=category.parent_category_id)
        return category_out


class GetCategoryCommand(BaseCategoryCommand):
    def __init__(self, category_id: int, session: AsyncSession):
        super().__init__(session)
        self.category_id = category_id

    async def execute(self) -> CategoryOut:
        category = await self.repo.get_category_by_id(self.category_id)

        if not category:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=ErrorMessage.CATEGORY_NOT_FOUND)
        category_out = CategoryOut(id=category.id, name=category.name, parent_category_id=category.parent_category_id)

        return category_out


class GetCategoryListCommand(BaseCategoryCommand):
    def __init__(self, offset: int, limit: int, session: AsyncSession):
        super().__init__(session)
        self.offset = offset
        self.limit = limit

    async def execute(self) -> list[CategoryOut]:
        categories = await self.repo.list_categories(self.offset, self.limit)
        result = [
            CategoryOut(
                id=category.id,
                name=category.name,
                parent_category_id=category.parent_category_id,
            )
            for category in categories
        ]
        return result
