from datetime import datetime

import sqlalchemy as sa
from db.helpers import get_mappings
from db.utils import session_manager
from sqlalchemy.dialects.postgresql import insert
from stats.datatypes import StatResponse
from stats.models import ProjectStat


class StatRepository:
    async def upsert(self, stats: list["Stat"]) -> None:
        async with session_manager() as session:
            for stat in stats:
                query = (
                    insert(ProjectStat)
                    .values(
                        user_id=stat.user_id,
                        project_id=stat.project_id,
                        count=stat.count,
                        date=stat.date,
                    )
                    .on_conflict_do_update(
                        "project_stats_unique",
                        set_=dict(count=ProjectStat.count + stat.count),
                    )
                )
                await session.execute(query)

    async def get_stats(
        self,
        user_id: str,
        project_id: int,
        begin: datetime,
        end: datetime,
        group_by_day: bool = False,
    ) -> list[StatResponse]:
        async with session_manager():
            query = (
                sa.select(ProjectStat.count, ProjectStat.date)
                .where(ProjectStat.user_id == user_id)
                .where(ProjectStat.project_id == project_id)
                .where(ProjectStat.date >= begin)
                .where(ProjectStat.date <= end)
                .order_by(ProjectStat.date.asc())
            )

            results = await get_mappings(query)

            if group_by_day and results:
                temp = []
                row = results.pop(0)
                current_date = row["date"].replace(
                    hour=0, minute=0, second=0, microsecond=0
                )
                current_count = row["count"]
                while results:
                    row = results.pop(0)
                    if (
                        row["date"].day != current_date.day
                        or row["date"].month != current_date.month
                        or row["date"].year != current_date.year
                    ):
                        temp.append(
                            {
                                "date": current_date,
                                "count": current_count,
                            }
                        )
                        current_date = row["date"].replace(
                            hour=0, minute=0, second=0, microsecond=0
                        )
                        current_count = row["count"]
                    else:
                        current_count += row["count"]
                temp.append(
                    {
                        "date": current_date,
                        "count": current_count,
                    }
                )
                results = temp

            return [StatResponse(**row) for row in results]

    async def get_total_stats(
        self, user_id: str, project_id: int, begin: datetime, end: datetime
    ) -> int:
        count = 0
        stats = await self.get_stats(user_id, project_id, begin, end)
        for row in stats:
            count += row.count
        return count


stat_repository = StatRepository()
