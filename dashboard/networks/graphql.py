import strawberry
from networks.datatypes import NetworkResponse
from networks.repository import network_repository


@strawberry.type
class Query:
    @strawberry.field()
    async def networks() -> list[NetworkResponse]:
        networks = await network_repository.get_all()
        return [NetworkResponse.from_db(row) for row in networks]
