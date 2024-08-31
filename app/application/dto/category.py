from pydantic import BaseModel


class CategoryIn(BaseModel):
    name: str
    parent_category_id: int | None = None


class CategoryOut(CategoryIn):
    id: int
