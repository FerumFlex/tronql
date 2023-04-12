from dataclasses import dataclass
from datetime import datetime

import strawberry
from common.permissions import IsAuthenticated
from stats import utils
from strawberry.types import Info


@dataclass
class Stat:
    project_id: int
    user_id: str
    date: datetime
    count: int


@strawberry.type
class ProjectStat:
    total: int
    begin: datetime
    end: datetime


@strawberry.type
class StatResponse:
    date: datetime
    count: int


@strawberry.federation.type(keys=["id"])
class ProjectResponse:
    id: strawberry.ID
    created_at: datetime = strawberry.federation.field(external=True)

    @strawberry.federation.field(
        requires=["createdAt"], permission_classes=[IsAuthenticated]
    )
    async def current_stats(self, info: Info) -> ProjectStat:
        created = datetime.fromisoformat(self.created_at)
        billing_cycle_start, billing_cycle_end = utils.get_current_biling_period(
            created
        )

        from stats.repository import stat_repository  # noqa

        count = await stat_repository.get_total_stats(
            info.context.user.id,
            int(self.id),
            billing_cycle_start,
            billing_cycle_end,
        )
        return ProjectStat(
            total=count,
            begin=billing_cycle_start,
            end=billing_cycle_end,
        )
