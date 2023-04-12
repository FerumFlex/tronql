import base64
from datetime import datetime, timezone

import redis.asyncio as redis
from stats import utils
from stats.datatypes import Stat


class Stats:
    _redis_url: str = None
    _redis: any

    def __init__(self, redis_url: str) -> None:
        self._redis_url = redis_url
        self._redis = None

    async def init(self) -> None:
        self._redis = await redis.from_url(
            self._redis_url, db=1, encoding="utf-8", decode_responses=True
        )

    async def track(self, user_id: str, project_id: int) -> None:
        date = utils.round_hour_datetime(datetime.now(timezone.utc)).isoformat()
        data = f"{user_id}|{project_id}|{date}"
        key = base64.encodebytes(data.encode("utf8")).decode("utf8").strip()
        await self._redis.incr(f"stats:{key}")

    async def process(self) -> list[Stat]:
        err, items = await self._redis.scan(0, "stats:*")
        if err:
            raise Exception(err)

        result = []
        for item in items:
            key = item.removeprefix("stats:")
            data = base64.decodebytes(key.encode("utf8")).decode("utf8")
            user_id, project_id, date = data.split("|")
            count = await self._redis.getdel(item)

            project_id = int(project_id)
            count = int(count)
            date = datetime.fromisoformat(date)
            result.append(
                Stat(user_id=user_id, project_id=project_id, date=date, count=count)
            )
        return result

    async def check_health(self) -> bool:
        return await self._redis.execute_command("PING")
