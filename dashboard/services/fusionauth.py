import http
import random
import string

from aiohttp import ClientResponseError
from auth.datatypes import UserInfo
from services.base import BaseService
from slugify import slugify


class FusionAuthError(Exception):
    pass


class FusionAuthService(BaseService):
    def __init__(self, base_url: str, api_key: str, app_id: str) -> None:
        self.app_id = app_id
        self.api_key = api_key
        super().__init__(base_url, headers={"Authorization": api_key})

    async def process_error(self, data: dict | str) -> None:
        if type(data) == dict and "fieldErrors" in data:
            parts = []
            for _, errors in data["fieldErrors"].items():
                for error in errors:
                    parts.append(error["message"])
            if data["generalErrors"]:
                parts.extend(data["generalErrors"])
            raise FusionAuthError("\n".join(parts))

    async def login(self, email: str, password: str) -> dict | None:
        try:
            data = {
                "loginId": email,
                "password": password,
                "applicationId": self.app_id,
            }
            return await self._request("POST", "/api/login", json=data)
        except ClientResponseError as ex:
            if ex.status == http.HTTPStatus.NOT_FOUND:
                return None
            raise ex

    async def signup(self, email: str, password: str) -> dict:
        username = slugify(email) + "".join(
            random.choices(string.ascii_lowercase + string.digits, k=5)
        )
        data = {
            "user": {
                "email": email,
                "password": password,
                "username": username,
                "data": UserInfo().dict(),
            },
            "skipRegistrationVerification": False,
            "skipVerification": False,
            "registration": {
                "applicationId": self.app_id,
                "roles": ["user"],
            },
        }
        return await self._request("POST", "/api/user/registration", json=data)

    async def verify_email(self, verification_id: str) -> bool:
        try:
            await self._request(
                "POST",
                "/api/user/verify-registration",
                json={
                    "verificationId": verification_id,
                },
                as_json=False,
            )
            return True
        except ClientResponseError as ex:
            if ex.status == http.HTTPStatus.NOT_FOUND:
                return False
            raise ex

    async def resend_verify_email(self, email: str) -> dict:
        return await self._request(
            "PUT",
            "/api/user/verify-registration",
            params={
                "applicationId": self.app_id,
                "email": email,
            },
            headers={"Content-Type": "application/json"},
        )

    async def me(self, header: str) -> dict | None:
        header = (header or "").strip()
        if " " not in header:
            return None

        category, token = header.split(" ", maxsplit=1)
        if category.lower() != "bearer":
            return None

        try:
            return await self._request(
                "GET",
                "/api/user",
                headers={"Authorization": f"Bearer {token}"},
            )
        except ClientResponseError as ex:
            if ex.status == http.HTTPStatus.UNAUTHORIZED:
                return None
            raise ex

    async def forgot_password(self, email: str) -> dict | None:
        try:
            return await self._request(
                "POST",
                "/api/user/forgot-password",
                json={
                    "loginId": email,
                    "sendForgotPasswordEmail": True,
                    "applicationId": self.app_id,
                },
                headers={"Content-Type": "application/json"},
            )
        except ClientResponseError as ex:
            if ex.status == http.HTTPStatus.NOT_FOUND:
                return None
            raise ex

    async def change_password(self, change_id: str, password: str) -> dict:
        return await self._request(
            "POST",
            f"/api/user/change-password/{change_id}",
            json={
                "password": password,
                "applicationId": self.app_id,
            },
            headers={"Content-Type": "application/json"},
            as_json=False,
        )

    async def refresh_token(self, refresh_token: str) -> dict:
        return await self._request(
            "POST",
            "/api/jwt/refresh",
            headers={
                "Cookie": f"refresh_token={refresh_token}",
                "Content-Type": "application/json",
            },
        )

    async def update_user_data(self, user_id: str, data: dict) -> dict:
        params = {
            "user": {
                "data": data,
            }
        }
        return await self._request(
            "PATCH",
            f"/api/user/{user_id}",
            json=params,
            headers={
                "Content-Type": "application/json",
            },
        )
