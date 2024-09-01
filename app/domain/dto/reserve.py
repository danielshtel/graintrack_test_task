from uuid import UUID

from pydantic import BaseModel, Field

from app.domain.dto import ProductOut


class ReserveIn(BaseModel):
    product_id: int
    quantity: int = Field(..., gt=0, description="Reserved quantity must be greater than 0")


class ReserveOut(BaseModel):
    id: int
    product: ProductOut
    user_id: UUID
    quantity: int
