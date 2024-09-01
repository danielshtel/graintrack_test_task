from typing import (
    Generic,
    TypeVar,
)

from pydantic import BaseModel

T = TypeVar('T')


class ServiceResponse(BaseModel, Generic[T]):
    data: T | list[T] = None
