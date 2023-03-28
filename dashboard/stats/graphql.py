from datetime import datetime, timedelta, timezone

import strawberry
from common.errors import ValidationError
from common.permissions import IsAuthenticated
from stats.datatypes import StatResponse
from stats.repository import stat_repository
from strawberry.types import Info


@strawberry.type
class Query:
    @strawberry.field(permission_classes=[IsAuthenticated])
    async def get_stats(
        info: Info, project_id: int, begin: datetime, end: datetime | None = None
    ) -> list[StatResponse]:
        if not end:
            end = datetime.now(timezone.utc)

        if end - begin > timedelta(days=180):
            raise ValidationError(
                f"Begin and end should not be differs more than 180 days"
            )

        results = await stat_repository.get_stats(
            info.context.user.id, project_id, begin, end
        )
        return [StatResponse.from_db(row) for row in results]

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
