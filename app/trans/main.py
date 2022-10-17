import datetime
from typing import List, Optional

import strawberry
from strawberry.scalars import JSON
import sentry

from trans import db


@strawberry.federation.type(keys=["transactionId"])
class TransactionLite:
    transaction_id: strawberry.ID
    block_hash: str
    time_stamp: datetime.datetime
    block_number: int
    energy_usage: int
    energy_fee: int
    origin_energy_usage: int
    energy_usage_total: int
    net_usage: int
    net_fee: int
    result: str | None
    trigger_name: str | None
    contract_address: str | None
    contract_type: str | None
    fee_limit: int
    contract_call_value: int
    contract_result: str | None
    from_address: str | None
    to_address: str | None
    asset_name: str | None
    asset_amount: int | None
    internal_transaction_list: JSON
    data: str | None
    transaction_index: int
    cumulative_energy_used: int
    pre_cumulative_log_count: int
    log_list: JSON
    energy_unit_price: int


@strawberry.federation.type(keys=["transactionId"])
class TransactionFull(TransactionLite):
    pass


@strawberry.federation.type(keys=["hash"])
class BlockFull:
    hash: strawberry.ID

    @strawberry.field
    async def transactions(root: "BlockFull") -> List[TransactionLite]:
        return await db.get_transactions_by_block_hash(root.hash)

    @classmethod
    def resolve_reference(cls, hash: strawberry.ID):
        return BlockFull(hash=hash)


@strawberry.type
class Query:
    @strawberry.field
    async def getTransactionByHash(hash: str) -> Optional[TransactionLite]:
        return await db.get_transaction_by_hash(hash)


schema = strawberry.federation.Schema(
    query=Query,
    types=[BlockFull],
    enable_federation_2=True,
)
