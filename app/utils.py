import re
import datetime
import base58


def from_timestamp(value: str | None) -> datetime:
    if not value:
        return None
    return datetime.datetime.fromtimestamp(int(value) / 1000)


def camel_to_snake_str(name: str) -> str:
    name = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", name)
    return re.sub("([a-z0-9])([A-Z])", r"\1_\2", name).lower()


def camel_to_snake_dict(value: dict) -> dict:
    return {camel_to_snake_str(k): v for k, v in value.items()}


def to_base58(address):
    return base58.b58encode_check(bytes.fromhex("41" + address[2:])).decode("utf8")
