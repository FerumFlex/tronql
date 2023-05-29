import json
import pathlib

import base58
from eth_abi import abi
from web3 import Web3

ABIS_DIR = pathlib.Path(__file__).parent / "abis"


def to_base58(address: str) -> str:
    address = address.removeprefix("0x")
    address = address.removeprefix("x")
    if not address.startswith("41"):
        address = "41" + address
    return base58.b58encode_check(bytes.fromhex(address)).decode("utf8")


def keccak256(text: str) -> str:
    return Web3.keccak(text=text).hex()


def decode_params(data: str, params: list[str]) -> list[any]:
    return abi.decode(params, bytes.fromhex(data))


def load_abi(name: str) -> dict:
    with open(ABIS_DIR / f"{name}.json", mode="r") as f:
        return json.load(f)
