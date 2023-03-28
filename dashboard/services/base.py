import asyncio
import http

import aiohttp


class BaseService:
    base_url = None
    session = None

    def __init__(self, base_url: str, headers: dict = None, retries: int = 0) -> None:
        self.base_url = base_url
        self.headers = headers
        self.retries = retries

    async def __aenter__(self):
        self.session = aiohttp.ClientSession(self.base_url, headers=self.headers)
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.session.close()

    async def process_error(self, data: dict | str) -> None:
        pass

    async def _request(
        self,
        method: str,
        path: str,
        json: dict = None,
        params: dict = None,
        retries: int = 0,
        headers: dict = None,
        as_json: bool = True,
    ) -> dict | str:
        retries = retries or self.retries or 0
        async with self.session.request(
            method,
            path,
            json=json,
            params=params,
            headers=headers,
        ) as response:
            try:
                try:
                    data = await response.json()
                except aiohttp.ContentTypeError:
                    data = await response.text()

                if response.status < 200 or response.status > 299:
                    await self.process_error(data)

                response.raise_for_status()
                return data
            except aiohttp.ClientResponseError as exc:
                if retries:
                    if (
                        exc.status == http.HTTPStatus.TOO_MANY_REQUESTS.value
                        and retries
                    ):
                        await asyncio.sleep(5)
                    else:
                        await asyncio.sleep(0.4)
                    return await self._request(method, path, data, retries=retries - 1)

                raise exc
