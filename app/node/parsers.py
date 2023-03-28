import json

from node.datatypes import (
    Account,
    AccountAsset,
    AccountFrozenBalance,
    AccountResources,
    AccountVote,
    Block,
    BlockHeader,
    Event,
    Node,
    Transaction,
    TransactionConsume,
    TransactionContract,
    TransactionContractParameter,
    TransactionContractParameterValue,
    TransactionInfo,
    TransactionInternal,
    TransactionRawData,
    TransactionResult,
    Witnes,
)
from utils import from_timestamp, to_base58


def parse_block(data: dict) -> Block:
    result = Block(
        blockID=data["blockID"],
        blockHeader=BlockHeader(
            witness_signature=data["block_header"]["witness_signature"],
            witness_address=to_base58(
                data["block_header"]["raw_data"]["witness_address"]
            ),
            number=data["block_header"]["raw_data"]["number"],
            txTrieRoot=data["block_header"]["raw_data"]["txTrieRoot"],
            parentHash=data["block_header"]["raw_data"]["parentHash"],
            version=data["block_header"]["raw_data"].get("version"),
            timestamp=from_timestamp(data["block_header"]["raw_data"].get("timestamp")),
        ),
        transactions=[parse_transaction(row) for row in data.get("transactions", [])],
    )
    return result


def parse_account(data: dict) -> Account:
    result = Account(
        votes=[AccountVote(**row) for row in data.get("votes", [])],
        frozen=[
            AccountFrozenBalance(
                expire_time=from_timestamp(row.get("expire_time")), **row
            )
            for row in data.get("frozen", [])
        ],
        frozen_supply=[
            AccountFrozenBalance(
                expire_time=from_timestamp(row.get("expire_time")), **row
            )
            for row in data.get("frozen_supply", [])
        ],
        assetV2=[AccountAsset(**row) for row in data.get("assetV2", [])],
        free_asset_net_usageV2=[
            AccountAsset(**row) for row in data.get("free_asset_net_usageV2", [])
        ],
        latest_opration_time=from_timestamp(data.get("latest_opration_time"))
        if "latest_opration_time" in data
        else None,
        latest_consume_time=from_timestamp(data.get("latest_consume_time"))
        if "latest_consume_time" in data
        else None,
        latest_consume_free_time=from_timestamp(data.get("latest_consume_free_time"))
        if "latest_consume_free_time" in data
        else None,
        account_name=data.get("account_name"),
        type=data.get("type"),
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
    assetNetUsed = data.get("assetNetUsed", [])
    assetNetLimit = data.get("assetNetLimit", [])
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
    raw_data = data.get("raw_data")
    result = Transaction(
        raw_data=TransactionRawData(
            expiration=from_timestamp(raw_data.get("expiration")),
            timestamp=from_timestamp(raw_data.get("timestamp")),
            contract=[
                TransactionContract(
                    parameter=TransactionContractParameter(
                        value=TransactionContractParameterValue(
                            data=row["parameter"]["value"].get("data"),
                            is_add_approval=row["parameter"]["value"].get(
                                "is_add_approval"
                            ),
                            proposal_id=row["parameter"]["value"].get("proposal_id"),
                            owner_address=to_base58(
                                row["parameter"]["value"]["owner_address"]
                            ),
                            contract_address=to_base58(
                                row["parameter"]["value"].get("contract_address")
                            )
                            if row["parameter"]["value"].get("contract_address")
                            else None,
                        ),
                        type_url=row["parameter"]["type_url"],
                    ),
                    type=row["type"],
                )
                for row in raw_data.get("contract", [])
            ],
            ref_block_bytes=raw_data["ref_block_bytes"],
            ref_block_hash=raw_data["ref_block_hash"],
            fee_limit=raw_data.get("fee_limit"),
        ),
        raw_data_hex=data["raw_data_hex"],
        ret=[
            TransactionResult(contractRet=row["contractRet"])
            for row in data.get("ret", [])
        ],
        signature=data["signature"],
        txID=data["txID"],
    )
    return result


def parse_transaction_info(data: dict) -> Transaction:
    receipt = data.get("receipt", {})
    result = TransactionInfo(
        blockTimeStamp=from_timestamp(data.get("blockTimeStamp")),
        internal_transactions=[
            TransactionInternal(
                callValueInfo=json.dumps(row.get("callValueInfo")), **row
            )
            for row in data.get("internal_transactions", [])
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


def parse_node(data: dict) -> Node:
    return Node(
        host=data["address"]["host"],
        port=data["address"]["port"],
    )
