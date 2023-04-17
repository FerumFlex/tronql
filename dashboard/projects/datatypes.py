from datetime import datetime
from decimal import Decimal
from typing import Self

import strawberry
from projects.repository import plan_repository
from strawberry.dataloader import DataLoader


@strawberry.federation.type(keys=["id"])
class PlanResponse:
    id: strawberry.ID
    slug: str

    created_at: datetime
    updated_at: datetime

    requests_per_month: int
    rate_limit: int
    rate_period: int

    title: str | None
    description: str | None

    visibility: str
    price: Decimal | None
    currency: str | None

    @classmethod
    def from_db(cls, instance) -> Self:
        return cls(**instance.to_dict())


async def load_plans(keys: list[int]) -> list[PlanResponse]:
    rows = await plan_repository.get_by_ids(keys)
    mapping = {row.id: PlanResponse.from_db(row) for row in rows if row}
    return [mapping.get(key) for key in keys]


PLAN_LOADER = DataLoader(load_fn=load_plans)


@strawberry.federation.type(keys=["slug"])
class NetworkResponse:
    slug: strawberry.ID


@strawberry.federation.type(keys=["id"])
class ProjectResponse:
    id: strawberry.ID
    name: str
    token: str
    user_id: str
    created_at: datetime
    updated_at: datetime

    plan_id: strawberry.Private[int]
    network_slug: strawberry.Private[str]

    @strawberry.field
    async def network(self) -> NetworkResponse:
        return NetworkResponse(slug=self.network_slug)

    @strawberry.field
    async def plan(self) -> PlanResponse:
        return await PLAN_LOADER.load(self.plan_id)

    @classmethod
    def from_db(cls, instance) -> Self:
        return cls(**instance.to_dict())

    @classmethod
    def from_dbs(cls, instances) -> list[Self]:
        return [cls.from_db(row) for row in instances]
