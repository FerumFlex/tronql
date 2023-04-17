import sqlalchemy as sa
from db.helpers import get_scalar, get_scalars
from db.utils import session_manager
from networks.models import Network


class NetworkRepository:
    async def get_by_ids(self, network_slugs: list[int]) -> list[Network]:
        async with session_manager():
            query = sa.select(Network).where(Network.slug.in_(network_slugs))
            return await get_scalars(query)

    async def get_all(self, filters: dict[str, any] | None = None) -> list[Network]:
        async with session_manager():
            query = sa.select(Network)
            if filters:
                for key, value in filters.items():
                    column = getattr(Network, key)
                    query = query.where(column == value)
            return await get_scalars(query)

    async def get_by_slug(self, slug: str) -> list[Network]:
        async with session_manager():
            query = sa.select(Network).where(Network.slug == slug)
            return await get_scalar(query)


network_repository = NetworkRepository()
