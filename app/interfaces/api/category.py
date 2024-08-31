from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.commands.category_command import CreateCategoryCommand, GetCategoryCommand
from app.application.dependencies.db import get_db_session
from app.application.dependencies.user import get_current_admin, get_current_user
from app.application.dto.category import CategoryOut, CategoryIn
from app.application.services.category import CategoryService
from app.core.config import settings
from app.core.generics import ServiceResponse
from app.domain.models import User

router = APIRouter(prefix=settings.CATEGORY_API_PREFIX, tags=['Category API'])

@router.post('/categories')
async def create_category(
    category_in: CategoryIn,
    current_admin: User = Depends(get_current_admin),
    session: AsyncSession = Depends(get_db_session)
) -> ServiceResponse[CategoryOut]:
    """Requires admin permissions"""
    category_command = CreateCategoryCommand(category_in, session)
    category_out = await category_command.execute()
    response = ServiceResponse(data=category_out)
    return response


@router.get('/categories')
async def list_categories(
    offset: int = 0,
    limit: int = 10,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db_session)
) -> ServiceResponse[list[CategoryOut]]:
    category_service = CategoryService(session)
    categories_out = await category_service.list_categories(offset, limit)
    response = ServiceResponse(data=categories_out)
    return response


@router.get('/categories/{category_id}')
async def get_category(
    category_id: int,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db_session)
) -> ServiceResponse[CategoryOut]:
    category_command = GetCategoryCommand(category_id, session)
    category_out = await category_command.execute()
    response = ServiceResponse(data=category_out)
    return response
