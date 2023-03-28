from fastapi import Depends, Request
from strawberry.fastapi import BaseContext


class CustomContext(BaseContext):
    def __init__(self, token: str | None):
        self.token = token


async def custom_context_dependency(request: Request) -> CustomContext:
    token = request.headers.get("authorization")
    return CustomContext(token=token)


async def get_custom_context(custom_context=Depends(custom_context_dependency)):
    return custom_context
