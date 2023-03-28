import json

from common.datatypes import User
from fastapi import Depends, Request
from strawberry.fastapi import BaseContext


class CustomContext(BaseContext):
    def __init__(self, user: User | None):
        self.user = user


async def user_context_dependency(request: Request) -> CustomContext:
    user = None

    user_data = request.headers.get("x-current-user") or ""
    if user_data:
        try:
            data = json.loads(user_data)
            user = User(**data)
        except json.JSONDecodeError:
            pass
    return CustomContext(user=user)


async def get_user_context(user_context=Depends(user_context_dependency)):
    return user_context
