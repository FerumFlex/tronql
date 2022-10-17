import http
import asyncio

import aiohttp


class BaseService:
    base_url = None
    session = None

    def __init__(self, base_url) -> None:
        self.base_url = base_url

    async def __aenter__(self):
        self.session = aiohttp.ClientSession(self.base_url)
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.session.close()

    async def _request(self, method, path, data=None, retries=5, headers=None):
        async with self.session.request(
            method,
            path,
            json=data if method != "get" else None,
            params=data if method == "get" else None,
            headers=headers,
        ) as response:
            try:
                response.raise_for_status()
                json_body = await response.json()
                return json_body
            except aiohttp.ClientResponseError as exc:
                if retries:
                    if exc.status == http.HTTPStatus.TOO_MANY_REQUESTS.value and retries:
                        await asyncio.sleep(5)
                    else:
                        await asyncio.sleep(0.4)
                    return await self._request(method, path, data, retries=retries - 1)

                raise exc
