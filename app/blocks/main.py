import datetime
from typing import List, Optional

import strawberry
import sentry

from blocks import db
from datatypes import BlocksFilter


@strawberry.federation.type(keys=["hash"])
class BlockLite:
    hash: strawberry.ID
    number: int
    timestamp: datetime.datetime
    transaction_ids: List[str]


@strawberry.federation.type(keys=["hash"])
class BlockFull(BlockLite):
    pass


@strawberry.type
class Query:
    @strawberry.field
    async def getBlocks(params: BlocksFilter) -> List[BlockLite]:
        params.validate()
        return await db.get_blocks(params)

    @strawberry.field
    async def getBlockById(number: int) -> Optional[BlockFull]:
        return await db.get_block_by_id(number)

    @strawberry.field
    async def getBlockByHash(hash: str) -> Optional[BlockFull]:
        return await db.get_block_by_hash(hash)

    @strawberry.field
    async def getLastestBlock() -> Optional[BlockFull]:
        return await db.get_latest_block()


schema = strawberry.federation.Schema(query=Query, enable_federation_2=True)
