from decimal import Decimal

from pydantic import BaseModel, Field


class ProductIn(BaseModel):
    name: str
    description: str
    price: Decimal = Field(..., gt=0, description="Price must be greater than 0")
    stock_quantity: int = Field(..., ge=0, description="Stock quantity must be greater than 0")
    category_id: int


class ProductUpdate(ProductIn):
    is_active: bool = True
    is_discount: bool = False
    discount_percent: Decimal | None


class ProductOut(ProductUpdate):
    id: int
    discount_price: Decimal