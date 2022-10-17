from typing import List
import datetime
from enum import Enum
import strawberry


class ValidationError(Exception):
    def __init__(self, field: str, message: str):
        super().__init__(message)
        self.field = field


@strawberry.enum
class Direction(Enum):
    asc = "asc"
    desc = "desc"


@strawberry.enum
class BlockOrderField(Enum):
    number = "number"


@strawberry.input
class PaginationInput:
    limit: int = 50
    offset: int = 0

    def validate(self) -> None:
        if not 0 <= self.limit <= 100:
            raise ValidationError("pagination.limit", "Should be from 0 to 100")
        if self.offset < 0:
            raise ValidationError("pagination.offset", "Should be greater than 0")


@strawberry.input
class BlockOrderInput:
    field: BlockOrderField = BlockOrderField.number
    direction: Direction = Direction.desc


@strawberry.input
class BlocksFilter:
    pagination: PaginationInput
    order: BlockOrderInput

    def validate(self) -> None:
        self.pagination.validate()
