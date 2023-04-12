from datetime import datetime, timedelta, timezone

import strawberry
from common.errors import ValidationError
from common.permissions import IsAuthenticated
from stats.datatypes import StatResponse
from stats.enums import StatsGroup
from stats.repository import stat_repository
from strawberry.types import Info


@strawberry.type
class Query:
    @strawberry.field(permission_classes=[IsAuthenticated])
    async def get_stats(
        info: Info,
        project_id: int,
        begin: datetime,
        end: datetime | None = None,
        group: StatsGroup = StatsGroup.hour,
    ) -> list[StatResponse]:
        if not end:
            end = datetime.now(timezone.utc)

        if end - begin > timedelta(days=90):
            raise ValidationError(
                f"Begin and end should not be differs more than 180 days"
            )

        if group == StatsGroup.hour:
            stick_date = begin.replace(minute=0, second=0, microsecond=0)
            delta = timedelta(hours=1)
            group_by_day = False
        elif group == StatsGroup.day:
            stick_date = begin.replace(hour=0, minute=0, second=0, microsecond=0)
            delta = timedelta(days=1)
            group_by_day = True

        results = await stat_repository.get_stats(
            info.context.user.id, project_id, stick_date, end, group_by_day
        )

        current = 0
        data = []
        while stick_date < end:
            row = results[current] if len(results) > current else None

            if row and stick_date >= row.date and stick_date < row.date + delta:
                data.append(row)
                current += 1
            else:
                item = StatResponse(
                    date=stick_date,
                    count=0,
                )
                data.append(item)
            stick_date += delta
        return data

    @strawberry.field(permission_classes=[IsAuthenticated])
    async def get_total_stats(
        info: Info, project_id: int, begin: datetime, end: datetime | None = None
    ) -> int:
        if not end:
            end = datetime.now(timezone.utc)

        if end - begin > timedelta(days=180):
            raise ValidationError(
                f"Begin and end should not be differs more than 180 days"
            )

        return await stat_repository.get_total_stats(
            info.context.user.id, project_id, begin, end
        )
