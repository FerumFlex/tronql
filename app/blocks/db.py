import sqlalchemy as sa
from db.utils import session_decorator

from datatypes import BlocksFilter
from models import Block


@session_decorator()
async def get_latest_block(session) -> Block | None:
    query = (
        sa.select(Block)
        .order_by(Block.number.desc())
        .limit(1)
    )
    result = await session.execute(query)
    return result.scalars().one_or_none()


@session_decorator()
async def get_blocks(session, params: BlocksFilter) -> list[Block]:
    order_field = getattr(Block, params.order.field.value)
    direction = getattr(order_field, params.order.direction.value)
    query = (
        sa.select(Block)
        .limit(params.pagination.limit)
        .offset(params.pagination.offset)
        .order_by(direction())
    )

    result = await session.execute(query)
    return result.scalars().all()


@session_decorator()
async def get_block_by_id(session, number: int) -> Block | None:
    query = (
        sa.select(Block)
        .where(Block.number == number)
    )

    result = await session.execute(query)
    return result.scalars().one_or_none()


@session_decorator()
async def get_block_by_hash(session, hash: str) -> Block | None:
    query = (
        sa.select(Block)
        .where(Block.hash == hash)
    )

    result = await session.execute(query)
    return result.scalars().one_or_none()
