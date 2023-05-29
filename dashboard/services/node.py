from services.base import BaseService


class TronNodeService(BaseService):
    def __init__(self, node_url: str, token: str) -> None:
        super().__init__(node_url, headers={"Authorization": token})

    async def validate_address(self, address: str) -> bool:
        result = await self._request(
            "post",
            "/wallet/validateaddress",
            {
                "address": address,
            },
        )
        return bool(result["result"])

    async def get_resources(self, address: str) -> dict | None:
        result = await self._request(
            "post",
            "/wallet/getaccountresource",
            {
                "address": address,
                "visible": True,
            },
        )
        return result if result else None

    async def get_account(self, address: str) -> dict | None:
        result = await self._request(
            "post",
            "/wallet/getaccount",
            {
                "address": address,
                "visible": True,
            },
        )
        return result if result else None

    async def get_block_by_hash(self, block_hash: str) -> dict | None:
        result = await self._request(
            "post",
            "/wallet/getblockbyid",
            {
                "detail": True,
                "value": block_hash,
            },
        )
        return result if result else None

    async def get_block_by_num(self, num: int) -> dict | None:
        result = await self._request(
            "post",
            "/wallet/getblockbynum",
            {
                "detail": True,
                "num": num,
            },
        )
        return result if result else None

    async def get_block_by_latest_num(self, num: int) -> list[dict]:
        result = await self._request(
            "post",
            "/wallet/getblockbylatestnum",
            {
                "num": num,
            },
        )
        return result["block"]

    async def get_lastest_block(self) -> dict | None:
        result = await self._request("post", "/wallet/getnowblock")
        return result if result else None

    async def get_blocks(self, start: int, end: int) -> list[dict]:
        result = await self._request(
            "post",
            "/wallet/getblockbylimitnext",
            {
                "startNum": start,
                "endNum": end,
            },
        )
        return result["block"] if result else []

    async def list_nodes(self) -> list[dict]:
        result = await self._request(
            "get",
            "/wallet/listnodes",
        )
        return result["nodes"]

    async def get_transaction(self, hash: str) -> dict | None:
        result = await self._request(
            "post",
            "/wallet/gettransactionbyid",
            {
                "value": hash,
            },
        )
        return result if result else None

    async def get_transaction_info(self, hash: str) -> dict | None:
        result = await self._request(
            "post",
            "/wallet/gettransactioninfobyid",
            {
                "value": hash,
            },
        )
        return result if result else None

    async def get_transaction_info_by_block(self, num: int) -> list[dict]:
        result = await self._request(
            "post",
            "/wallet/gettransactioninfobyblocknum",
            {
                "num": num,
            },
        )
        return result if result else None

    async def get_witnesses(self) -> list[dict]:
        result = await self._request("post", "/wallet/listwitnesses")
        return result["witnesses"]

    async def get_transaction_events(self, hash: str) -> list[dict] | None:
        result = await self._request("get", f"/v1/transactions/{hash}/events")
        return result["data"] if result else None
