import datetime
from typing import List

import strawberry
from strawberry.scalars import JSON


@strawberry.type
class BlockHeader:
    number: int
    txTrieRoot: str
    witness_address: str
    witness_signature: str
    parentHash: str
    version: int | None = None
    timestamp: datetime.datetime | None = None


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
    expire_time: datetime.datetime | None


@strawberry.type
class Account:
    account_name: str | None = None
    type: str | None = None
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
    expiration: datetime.datetime | None
    fee_limit: int | None = None
    timestamp: datetime.datetime | None
    contract: List[TransactionContract]


@strawberry.type
class Transaction:
    signature: List[str]
    txID: str
    ret: List[TransactionResult]
    raw_data: TransactionRawData
    raw_data_hex: str


@strawberry.type
class TransactionLog:
    address: str
    data: str
    topics: list[str] = None


@strawberry.type
class TransactionInfo:
    id: str
    fee: float | None = None
    blockNumber: int
    blockTimeStamp: datetime.datetime | None
    contractResult: list[str]
    contract_address: str | None = None
    receipt: TransactionConsume
    result: str | None = None
    resMessage: str | None = None
    internal_transactions: List[TransactionInternal]
    log: list[TransactionLog] | None


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
class Block:
    blockID: str
    blockHeader: BlockHeader
    transactions: List[Transaction] | None = None


@strawberry.type
class Event:
    block_number: int
    block_timestamp: datetime.datetime | None
    caller_contract_address: str
    contract_address: str
    event_index: int
    event_name: str
    result: JSON
    result_type: JSON
    event: str
    transaction_id: str


@strawberry.type
class Node:
    host: str
    port: int
