from typing import Generic, List, TypeVar

import strawberry
from pydantic import BaseModel

T = TypeVar("T")


class UserInfo(BaseModel):
    plan_slug: str = "basic"


class User(BaseModel):
    id: str
    active: bool
    verified: bool
    data: UserInfo | None
    email: str
    first_name: str | None
    last_name: str | None


@strawberry.type
class PaginationResponse(Generic[T]):
    list: List[T]
    count: int
    limit: int
    offset: int
