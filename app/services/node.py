from services.base import BaseService
from config import settings


class TronNodeService(BaseService):
    def __init__(self) -> None:
        super().__init__(settings.tron_node_url)

    async def validate_address(self, address: str) -> bool:
        result = await self._request("post", "/wallet/validateaddress", {
            "address": address,
        })
        return bool(result["result"])

    async def get_resources(self, address: str) -> dict | None:
        result = await self._request("post", "/wallet/getaccountresource", {
            "address": address,
            "visible": True,
        })
        return result if result else None

    async def get_account(self, address: str) -> dict | None:
        result = await self._request("post", "/wallet/getaccount", {
            "address": address,
            "visible": True,
        })
        return result if result else None

    async def get_block_by_hash(self, id_or_hash: str) -> dict | None:
        result = await self._request("post", "/wallet/getblock", {
            "detail": True,
            "id_or_num": id_or_hash,
        })
        return result if result else None

    async def get_lastest_block(self) -> dict | None:
        result = await self._request("post", "/wallet/getnowblock")
        return result if result else None

    async def get_blocks(self, start: int, end: int) -> list[dict]:
        result = await self._request("post", "/wallet/getblockbylimitnext", {
            "startNum": start,
            "endNum": end,
        })
        return result["block"] if result else []

    async def get_transaction(self, hash: str) -> dict | None:
        result = await self._request("post", "/wallet/gettransactionbyid", {
            "value": hash,
        })
        return result if result else None

    async def get_transaction_info(self, hash: str) -> dict | None:
        result = await self._request("post", "/wallet/gettransactioninfobyid", {
            "value": hash,
        })
        return result if result else None

    async def get_transaction_info_by_block(self, num: int) -> list[dict]:
        result = await self._request("post", "/wallet/gettransactioninfobyblocknum", {
            "num": num,
        })
        return result if result else None

    async def get_witnesses(self) -> list[dict]:
        result = await self._request("post", "/wallet/listwitnesses")
        return result["witnesses"]

    async def get_transaction_events(self, hash: str) -> list[dict] | None:
        result = await self._request("get", f"/v1/transactions/{hash}/events")
        return result["data"] if result else None
