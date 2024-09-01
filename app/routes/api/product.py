from fastapi import APIRouter, Depends, Query, Body
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.commands.product_command import (
    ListProductCommand,
    FilterProductCommand,
    GetProductCommand,
    CreateProductCommand,
    DeleteProductCommand,
    UpdateProductCommand
)
from app.application.commands.reserve import ReserveProductCommand, DereserveProductCommand
from app.application.dependencies.db import get_db_session
from app.application.dependencies.user import get_current_user, get_current_admin
from app.application.models import User
from app.core.config import settings
from app.core.generics import ServiceResponse
from app.domain.dto.product import ProductOut, ProductIn, ProductUpdate
from app.domain.dto.reserve import ReserveOut, ReserveIn

router = APIRouter(prefix=settings.PRODUCT_API_PREFIX, tags=['Product API'])


@router.get('/list')
async def get_product_list(
    offset: int = 0,
    limit: int = 10,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db_session)
) -> ServiceResponse[list[ProductOut]]:
    product_command = ListProductCommand(offset, limit, session)
    products = await product_command.execute()
    response = ServiceResponse(data=products)
    return response


@router.get('/filter')
async def filter_by_categories(
    categories_ids: list[int] = Query(...),
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db_session)
) -> ServiceResponse[list[ProductOut]]:
    product_command = FilterProductCommand(categories_ids, session)
    products = await product_command.execute()
    response = ServiceResponse(data=products)
    return response


@router.get('/{product_id}')
async def get_product_by_id(
    product_id: int,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db_session)
) -> ServiceResponse[ProductOut]:
    product_command = GetProductCommand(product_id, session)
    product = await product_command.execute()
    response = ServiceResponse(data=product)
    return response


@router.post('/')
async def create_product(
    product_in: ProductIn,
    current_user: User = Depends(get_current_admin),
    session: AsyncSession = Depends(get_db_session)
) -> ServiceResponse[ProductOut]:
    """Requires admin permissions"""
    command = CreateProductCommand(product_in, session)
    product = await command.execute()
    return ServiceResponse(data=product)


@router.put('/{product_id}')
async def update_product(
    product_id: int,
    product_update: ProductUpdate,
    current_user: User = Depends(get_current_admin),
    session: AsyncSession = Depends(get_db_session)
) -> ServiceResponse[ProductOut]:
    """Requires admin permissions"""
    command = UpdateProductCommand(product_id, product_update, session)
    product = await command.execute()
    return ServiceResponse(data=product)


@router.delete('/{product_id}')
async def delete_product(
    product_id: int,
    current_user: User = Depends(get_current_admin),
    session: AsyncSession = Depends(get_db_session)
) -> ServiceResponse:
    """Requires admin permissions"""
    command = DeleteProductCommand(product_id, session)
    await command.execute()
    return ServiceResponse()


@router.post('/reserve')
async def reserve_product(
    reserve_in: ReserveIn = Body(...),
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db_session)
) -> ServiceResponse[ReserveOut]:
    command = ReserveProductCommand(reserve_in, current_user.id, session)
    reserve = await command.execute()
    return ServiceResponse(data=reserve)


@router.delete('/de-reserve/{reserve_id}')
async def dereserve_product(
    reserve_id: int,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db_session)
) -> ServiceResponse[bool]:
    command = DereserveProductCommand(current_user.id, reserve_id, session)
    result = await command.execute()
    return ServiceResponse(data=result)
