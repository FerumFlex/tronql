import asyncio
from datetime import datetime, timezone
from zoneinfo import ZoneInfo

import sentry  # noqa
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from db.base import init_db
from logger import logger
from stats.config import settings
from stats.repository import stat_repository
from stats.stats import Stats

stats = Stats(settings.redis_url)


async def update_stats():
    now = datetime.now(timezone.utc)
    logger.info(f"Processing data {now}")

    data = await stats.process()
    if not data:
        return

    await stat_repository.upsert(data)


async def init():
    await asyncio.gather(
        init_db(settings.database_url),
        stats.init(),
    )


def start_scheduler():
    database_uri = settings.database_url.replace("+asyncpg", "")
    jobstores = {"stats": SQLAlchemyJobStore(url=database_uri, tablename="stats_jobs")}
    scheduler = AsyncIOScheduler(timezone=ZoneInfo("Europe/Kiev"), jobstores=jobstores)

    scheduler.add_job(
        update_stats,
        "cron",
        second="0",
        minute="*",
        id="update_stats",
        misfire_grace_time=60,
        replace_existing=True,
    )
    scheduler.start()


def run_scheduler():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(init())

    start_scheduler()

    try:
        loop.run_forever()
    except (KeyboardInterrupt, SystemExit):
        pass


if __name__ == "__main__":
    run_scheduler()
