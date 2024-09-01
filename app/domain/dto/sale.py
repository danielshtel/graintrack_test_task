from datetime import datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, Field

from app.core.constants import SortingOrder
from app.domain.dto import ProductOut


class SaleIn(BaseModel):
    product_id: int
    quantity: int = Field(..., gt=0, description="Buy quantity must be greater than 0")


class SaleOut(BaseModel):
    id: int
    product: ProductOut
    user_id: UUID
    quantity: int
    created_at: datetime


class SalesReportFilters(BaseModel):
    start_date: datetime | None = None
    end_date: datetime | None = None

    min_price: Decimal | None = None
    max_price: Decimal | None = None

    category_ids: list[int] = []
    product_ids: list[int] = []
    user_ids: list[int] = []

    order_by: SortingOrder =  SortingOrder.asc
    offset: int = Field(default=0, ge=0)
    limit: int = Field(default=10, ge=1)