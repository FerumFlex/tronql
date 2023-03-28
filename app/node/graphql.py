from typing import List, Optional

import strawberry
from node.datatypes import (
    Account,
    AccountResources,
    Block,
    Event,
    Node,
    Transaction,
    TransactionInfo,
    Witnes,
)
from node.parsers import (
    parse_account,
    parse_block,
    parse_event,
    parse_node,
    parse_resources,
    parse_transaction,
    parse_transaction_info,
    parse_witness,
)
from services.node import TronNodeService
from strawberry.types import Info


@strawberry.type
class Query:
    @strawberry.field
    async def validateAddress(address: str, info: Info) -> bool:
        node_service = TronNodeService(info.context.token)
        async with node_service:
            return await node_service.validate_address(address)

    @strawberry.field
    async def getResources(address: str, info: Info) -> Optional[AccountResources]:
        node_service = TronNodeService(info.context.token)
        async with node_service:
            data = await node_service.get_resources(address)
            return parse_resources(data) if data else None

    @strawberry.field
    async def getAccount(address: str, info: Info) -> Optional[Account]:
        node_service = TronNodeService(info.context.token)
        async with node_service:
            data = await node_service.get_account(address)
            return parse_account(data) if data else None

    @strawberry.field
    async def getBlockById(block_hash: str, info: Info) -> Optional[Block]:
        node_service = TronNodeService(info.context.token)
        async with node_service:
            data = await node_service.get_block_by_hash(block_hash)
            return parse_block(data) if data else None

    @strawberry.field
    async def getBlockByNum(num: int, info: Info) -> Optional[Block]:
        node_service = TronNodeService(info.context.token)
        async with node_service:
            data = await node_service.get_block_by_num(num)
            return parse_block(data) if data else None

    @strawberry.field
    async def getBlocksByLatestNum(num: int, info: Info) -> list[Block]:
        node_service = TronNodeService(info.context.token)
        async with node_service:
            data = await node_service.get_block_by_latest_num(num)
            return [parse_block(row) for row in data]

    @strawberry.field
    async def getLatestBlock(info: Info) -> Optional[Block]:
        node_service = TronNodeService(info.context.token)
        async with node_service:
            data = await node_service.get_lastest_block()
            return parse_block(data) if data else None

    @strawberry.field
    async def getBlocks(start: int, end: int, info: Info) -> List[Block]:
        node_service = TronNodeService(info.context.token)
        async with node_service:
            data = await node_service.get_blocks(start, end)
            return [parse_block(row) for row in data]

    @strawberry.field
    async def getTransactionByID(hash: str, info: Info) -> Optional[Transaction]:
        node_service = TronNodeService(info.context.token)
        async with node_service:
            data = await node_service.get_transaction(hash)
            return parse_transaction(data) if data else None

    @strawberry.field
    async def getTransactionInfoByID(
        hash: str, info: Info
    ) -> Optional[TransactionInfo]:
        node_service = TronNodeService(info.context.token)
        async with node_service:
            data = await node_service.get_transaction_info(hash)
            return parse_transaction_info(data) if data else None

    @strawberry.field
    async def getTransactionsInfoByBlockNum(
        num: int, info: Info
    ) -> List[TransactionInfo]:
        node_service = TronNodeService(info.context.token)
        async with node_service:
            data = await node_service.get_transaction_info_by_block(num)
            return [parse_transaction_info(row) for row in data]

    @strawberry.field
    async def getWitnesses(info: Info) -> List[Witnes]:
        node_service = TronNodeService(info.context.token)
        async with node_service:
            data = await node_service.get_witnesses()
            return [parse_witness(row) for row in data]

    @strawberry.field
    async def listNodes(info: Info) -> List[Node]:
        node_service = TronNodeService(info.context.token)
        async with node_service:
            data = await node_service.list_nodes()
            return [parse_node(row) for row in data]

    @strawberry.field
    async def getTransactionEvents(hash: str, info: Info) -> List[Event] | None:
        node_service = TronNodeService(info.context.token)
        async with node_service:
            data = await node_service.get_transaction_events(hash)
            return [parse_event(row) for row in data] if data else None


schema = strawberry.federation.Schema(query=Query, enable_federation_2=True)
