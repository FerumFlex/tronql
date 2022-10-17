from typing import List
import sqlalchemy as sa
from db.utils import session_decorator

from models import Transaction


@session_decorator()
async def get_transaction_by_hash(session, hash: str) -> Transaction | None:
    query = (
        sa.select(Transaction)
        .where(Transaction.transaction_id == hash)
    )

    result = await session.execute(query)
    return result.scalars().one_or_none()


@session_decorator()
async def get_transactions_by_block_hash(session, hash: str) -> List[Transaction]:
    query = (
        sa.select(Transaction)
        .where(Transaction.block_hash == hash)
    )

    result = await session.execute(query)
    return result.scalars().all()
