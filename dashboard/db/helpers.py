import sqlalchemy as sa
from db.base import current_session


async def get_count(query) -> int:
    count_query = (
        query.with_only_columns(sa.func.count()).order_by(None).limit(None).offset(None)
    )
    result = await current_session.execute(count_query)
    count = result.scalar() or 0
    return count


async def get_scalars(
    query, limit: int | None = None, offset: int | None = None
) -> list[any]:
    if limit is not None:
        query = query.limit(limit)
    if offset is not None:
        query = query.offset(offset)
    result = await current_session.execute(query)
    return result.scalars().all()


async def get_scalar(query) -> any:
    result = await current_session.execute(query)
    return result.scalars().one_or_none()
