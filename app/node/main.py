import json
import datetime
from typing import List, Optional

import strawberry
from strawberry.scalars import JSON
import sentry
from services.node import TronNodeService
from utils import from_timestamp, to_base58


@strawberry.type
class BlockHeader:
    number: int
    txTrieRoot: str
    witness_address: str
    witness_signature: str
    parentHash: str
    version: int
    timestamp: datetime.datetime


@strawberry.type
class Block:
    blockID: str
    blockHeader: BlockHeader


@strawberry.type
class AccountAsset:
    key: str
    value: float


@strawberry.type
class AccountResources:
    freeNetLimit: float
    NetLimit: float | None = None
    assetNetUsed: List[AccountAsset]
    assetNetLimit: List[AccountAsset]
    TotalNetLimit: float
    TotalNetWeight: float
    tronPowerUsed: float | None = None
    tronPowerLimit: float | None = None
    TotalEnergyLimit: float
    TotalEnergyWeight: float


@strawberry.type
class AccountVote:
    vote_address: str
    vote_count: float


@strawberry.type
class AccountFrozenBalance:
    frozen_balance: float
    expire_time: datetime.datetime


@strawberry.type
class Account:
    account_name: str
    type: str
    address: str
    balance: float | None = None
    votes: List[AccountVote]
    frozen: List[AccountFrozenBalance]
    latest_opration_time: datetime.datetime | None = None
    allowance: float | None = None
    frozen_supply: List[AccountFrozenBalance]
    asset_issued_name: str | None = None
    latest_consume_time: datetime.datetime | None = None
    latest_consume_free_time: datetime.datetime | None = None
    assetV2: List[AccountAsset]
    asset_issued_ID: str | None = None
    free_asset_net_usageV2: List[AccountAsset]


@strawberry.type
class TransactionConsume:
    energy_fee: int | None = None
    energy_usage_total: int | None = None
    net_usage: int | None = None
    result: str | None = None


@strawberry.type
class TransactionInternal:
    hash: str
    caller_address: str
    transferTo_address: str
    callValueInfo: List[str]
    note: str
    rejected: bool


@strawberry.type
class TransactionResult:
    contractRet: str


@strawberry.type
class TransactionContractParameterValue:
    data: str | None = None
    owner_address: str
    contract_address: str | None = None
    is_add_approval: bool | None = None
    proposal_id: int | None = None


@strawberry.type
class TransactionContractParameter:
    value: TransactionContractParameterValue
    type_url: str


@strawberry.type
class TransactionContract:
    parameter: TransactionContractParameter
    type: str


@strawberry.type
class TransactionRawData:
    ref_block_bytes: str
    ref_block_hash: str
    expiration: datetime.datetime
    fee_limit: int | None = None
    timestamp: datetime.datetime
    contract: List[TransactionContract]


@strawberry.type
class Transaction:
    signature: List[str]
    txID: str
    ret: List[TransactionResult]
    raw_data: TransactionRawData
    raw_data_hex: str


@strawberry.type
class TransactionInfo:
    id: str
    fee: float | None = None
    blockNumber: int
    blockTimeStamp: datetime.datetime
    contractResult: list[str]
    contract_address: str | None = None
    receipt: TransactionConsume
    result: str | None = None
    resMessage: str | None = None
    internal_transactions: List[TransactionInternal]


@strawberry.type
class Witnes:
    address: str
    voteCount: float | None = None
    url: str
    totalProduced: int | None = None
    totalMissed: int | None = None
    latestBlockNum: int | None = None
    latestSlotNum: int | None = None
    isJobs: bool | None = None


@strawberry.type
class Event:
    block_number: int
    block_timestamp: datetime.datetime
    caller_contract_address: str
    contract_address: str
    event_index: int
    event_name: str
    result: JSON
    result_type: JSON
    event: str
    transaction_id: str


def parse_block(data: dict) -> Block:
    result = Block(
        blockID=data["blockID"],
        blockHeader=BlockHeader(
            witness_signature=data["block_header"]["witness_signature"],
            witness_address=to_base58(data["block_header"]["raw_data"]["witness_address"]),
            number=data["block_header"]["raw_data"]["number"],
            txTrieRoot=data["block_header"]["raw_data"]["txTrieRoot"],
            parentHash=data["block_header"]["raw_data"]["parentHash"],
            version=data["block_header"]["raw_data"]["version"],
            timestamp=from_timestamp(data["block_header"]["raw_data"].pop("timestamp")),
        )
    )
    return result


def parse_account(data: dict) -> Account:
    data.pop("account_resource")
    result = Account(
        votes=[AccountVote(**row) for row in data.pop("votes", [])],
        frozen=[AccountFrozenBalance(
            expire_time=from_timestamp(row.pop("expire_time")),
            **row) for row in data.pop("frozen", [])],
        frozen_supply=[AccountFrozenBalance(
            expire_time=from_timestamp(row.pop("expire_time")),
            **row) for row in data.pop("frozen_supply", [])],
        assetV2=[AccountAsset(**row) for row in data.pop("assetV2", [])],
        free_asset_net_usageV2=[AccountAsset(**row) for row in data.pop("free_asset_net_usageV2", [])],
        latest_opration_time=from_timestamp(data.pop("latest_opration_time")) if "latest_opration_time" in data else None,
        latest_consume_time=from_timestamp(data.pop("latest_consume_time")) if "latest_consume_time" in data else None,
        latest_consume_free_time=from_timestamp(data.pop("latest_consume_free_time")) if "latest_consume_free_time" in data else None,
        account_name=data["account_name"],
        type=data["type"],
        address=data["address"],
        balance=data.get("balance"),
        allowance=data.get("allowance"),
        asset_issued_name=data.get("asset_issued_name"),
        asset_issued_ID=data.get("asset_issued_ID"),
    )
    return result


def parse_account_asset(data: dict) -> AccountAsset:
    return AccountAsset(
        key=data["key"],
        value=data["value"],
    )


def parse_resources(data: dict) -> AccountResources:
    assetNetUsed = data.pop("assetNetUsed", [])
    assetNetLimit = data.pop("assetNetLimit", [])
    result = AccountResources(
        assetNetUsed=[parse_account_asset(r) for r in assetNetUsed],
        assetNetLimit=[parse_account_asset(r) for r in assetNetLimit],
        freeNetLimit=data["freeNetLimit"],
        NetLimit=data.get("NetLimit"),
        TotalNetLimit=data["TotalNetLimit"],
        TotalNetWeight=data["TotalNetWeight"],
        tronPowerUsed=data.get("tronPowerUsed"),
        tronPowerLimit=data.get("tronPowerLimit"),
        TotalEnergyLimit=data["TotalEnergyLimit"],
        TotalEnergyWeight=data["TotalEnergyWeight"],
    )
    return result


def parse_transaction(data: dict) -> Transaction:
    raw_data = data.pop("raw_data")
    result = Transaction(
        raw_data=TransactionRawData(
            expiration=from_timestamp(raw_data.pop("expiration")),
            timestamp=from_timestamp(raw_data.pop("timestamp")),
            contract=[TransactionContract(
                parameter=TransactionContractParameter(
                    value=TransactionContractParameterValue(
                        data=row["parameter"]["value"].get("data"),
                        is_add_approval=row["parameter"]["value"].get("is_add_approval"),
                        proposal_id=row["parameter"]["value"].get("proposal_id"),
                        owner_address=row["parameter"]["value"]["owner_address"],
                        contract_address=row["parameter"]["value"].get("contract_address"),
                    ),
                    type_url=row["parameter"]["type_url"],
                ),
                type=row["type"],
            ) for row in raw_data.pop("contract", [])],
            ref_block_bytes=raw_data["ref_block_bytes"],
            ref_block_hash=raw_data["ref_block_hash"],
            fee_limit=raw_data.get("fee_limit"),
        ),
        raw_data_hex=data["raw_data_hex"],
        ret=[TransactionResult(contractRet=row["contractRet"]) for row in data.pop("ret", [])],
        signature=data["signature"],
        txID=data["txID"],
    )
    return result


def parse_transaction_info(data: dict) -> Transaction:
    receipt = data.pop("receipt")
    result = TransactionInfo(
        blockTimeStamp=from_timestamp(data.pop("blockTimeStamp")),
        internal_transactions=[
            TransactionInternal(
                callValueInfo=json.dumps(row.pop("callValueInfo")),
                **row
            ) for row in data.pop("internal_transactions", [])
        ],
        receipt=TransactionConsume(
            energy_fee=receipt.get("energy_fee"),
            energy_usage_total=receipt.get("energy_usage_total"),
            net_usage=receipt.get("net_usage"),
            result=receipt.get("result"),
        ),
        **data,
    )
    return result


def parse_witness(data: dict) -> Witnes:
    return Witnes(
        address=to_base58(data["address"]),
        voteCount=data.get("voteCount"),
        url=data["url"],
        totalProduced=data.get("totalProduced"),
        totalMissed=data.get("totalMissed"),
        latestBlockNum=data.get("latestBlockNum"),
        latestSlotNum=data.get("latestSlotNum"),
        isJobs=data.get("isJobs"),
    )


def parse_event(data: dict) -> Event:
    return Event(
        block_number=data["block_number"],
        block_timestamp=from_timestamp(data["block_timestamp"]),
        caller_contract_address=data["caller_contract_address"],
        contract_address=data["contract_address"],
        event_index=data["event_index"],
        event_name=data["event_name"],
        result=data["result"],
        result_type=data["result_type"],
        event=data["event"],
        transaction_id=data["transaction_id"],
    )


@strawberry.type
class Query:
    @strawberry.field
    async def validateAddress(address: str) -> bool:
        node_service = TronNodeService()
        async with node_service:
            return await node_service.validate_address(address)

    @strawberry.field
    async def getResources(address: str) -> Optional[AccountResources]:
        node_service = TronNodeService()
        async with node_service:
            data = await node_service.get_resources(address)
            return parse_resources(data) if data else None

    @strawberry.field
    async def getAccount(address: str) -> Optional[Account]:
        node_service = TronNodeService()
        async with node_service:
            data = await node_service.get_account(address)
            return parse_account(data) if data else None

    @strawberry.field
    async def getBlock(id_or_hash: str) -> Optional[Block]:
        node_service = TronNodeService()
        async with node_service:
            data = await node_service.get_block_by_hash(id_or_hash)
            return parse_block(data) if data else None

    @strawberry.field
    async def getLatestBlock() -> Optional[Block]:
        node_service = TronNodeService()
        async with node_service:
            data = await node_service.get_lastest_block()
            return parse_block(data) if data else None

    @strawberry.field
    async def getBlocks(start: int, end: int) -> List[Block]:
        node_service = TronNodeService()
        async with node_service:
            data = await node_service.get_blocks(start, end)
            return [parse_block(row) for row in data]

    @strawberry.field
    async def getTransactionByID(hash: str) -> Optional[Transaction]:
        node_service = TronNodeService()
        async with node_service:
            data = await node_service.get_transaction(hash)
            return parse_transaction(data) if data else None

    @strawberry.field
    async def getTransactionInfoByID(hash: str) -> Optional[TransactionInfo]:
        node_service = TronNodeService()
        async with node_service:
            data = await node_service.get_transaction_info(hash)
            return parse_transaction_info(data) if data else None

    @strawberry.field
    async def getTransactionsInfoByBlockNum(num: int) -> List[TransactionInfo]:
        node_service = TronNodeService()
        async with node_service:
            data = await node_service.get_transaction_info_by_block(num)
            return [parse_transaction_info(row) for row in data]

    @strawberry.field
    async def getWitnesses() -> List[Witnes]:
        node_service = TronNodeService()
        async with node_service:
            data = await node_service.get_witnesses()
            return [parse_witness(row) for row in data]

    @strawberry.field
    async def getTransactionEvents(hash: str) -> List[Event] | None:
        node_service = TronNodeService()
        async with node_service:
            data = await node_service.get_transaction_events(hash)
            return [parse_event(row) for row in data] if data else None


schema = strawberry.federation.Schema(query=Query, enable_federation_2=True)
