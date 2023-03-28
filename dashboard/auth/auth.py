import json

from auth.config import settings
from auth.datatypes import User
from fastapi import APIRouter, Request
from services.fusionauth import FusionAuthService

router = APIRouter()


async def get_user(token: str) -> User | None:
    async with FusionAuthService(
        settings.fusion_api_url,
        settings.fusion_api_key,
        settings.fusion_app_id,
    ) as fusion:
        data = await fusion.me(token)
        if data:
            data = User.parse_obj(data["user"])
        return data


@router.post("/login")
async def main(request: Request):
    try:
        body = await request.json()
        authorization = body["headers"].get("authorization", [])
        authorization = authorization[0] if authorization else None
        current_user = await get_user(authorization)

        return {
            "version": body["version"],
            "stage": body["stage"],
            "control": "Continue",
            "id": body["id"],
            "headers": {
                "x-current-user": [current_user.json()] if current_user else [],
                "content-type": ["application/json"],
            },
            "context": body["context"],
            "body": body["body"],
            "sdl": body["sdl"],
        }
    except json.JSONDecodeError:
        return {"control": {"Break": 400}}
