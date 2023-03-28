import re
from datetime import datetime

import base58


def from_timestamp(value: str | None) -> datetime | None:
    if not value:
        return None

    try:
        return datetime.fromtimestamp(int(value) / 1000)
    except ValueError:
        return None


def camel_to_snake_str(name: str) -> str:
    name = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", name)
    return re.sub("([a-z0-9])([A-Z])", r"\1_\2", name).lower()


def camel_to_snake_dict(value: dict) -> dict:
    return {camel_to_snake_str(k): v for k, v in value.items()}


def to_base58(address):
    return base58.b58encode_check(bytes.fromhex("41" + address[2:])).decode("utf8")
