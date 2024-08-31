

from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import status, HTTPException

from app.application.commands.base_command import BaseCommand
from app.application.dto.category import CategoryOut, CategoryIn
from app.application.services.category import CategoryService
from app.core.constants import ErrorMessage


class BaseCategoryCommand(BaseCommand):
    def __init__(self, session: AsyncSession):
        self.session = session
        self.service = CategoryService(session)


class CreateCategoryCommand(BaseCategoryCommand):

    def __init__(self, category_in: CategoryIn, session: AsyncSession):
        super().__init__(session)
        self.category_in = category_in

    async def execute(self) -> CategoryOut:
        category = await self.service.create_category(self.category_in)
        category_out = CategoryOut(id=category.id, name=category.name, parent_category_id=category.parent_category_id)
        return category_out


class GetCategoryCommand(BaseCategoryCommand):
    def __init__(self, category_id: int, session: AsyncSession):
        super().__init__(session)
        self.category_id = category_id

    async def execute(self) -> CategoryOut:
        category = await self.service.get_category_by_id(self.category_id)

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
        categories = await self.service.list_categories(self.offset, self.limit)
        result = [
            CategoryOut(
                id=category.id,
                name=category.name,
                parent_category_id=category.parent_category_id,
            )
            for category in categories
        ]
        return result
