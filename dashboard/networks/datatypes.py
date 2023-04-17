from datetime import datetime
from typing import Self

import strawberry
from networks.repository import network_repository


@strawberry.federation.type(keys=["slug"])
class NetworkResponse:
    slug: strawberry.ID
    title: str
    domain: str
    header_in_domain: bool

    created_at: datetime
    updated_at: datetime

    @classmethod
    def from_db(cls, instance) -> Self:
        return cls(**instance.to_dict())

    @classmethod
    async def resolve_reference(cls, slug: strawberry.ID) -> "NetworkResponse":
        network = await network_repository.get_by_slug(slug)
        return NetworkResponse.from_db(network)
