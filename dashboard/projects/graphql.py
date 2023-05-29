import strawberry
import utils
from common.datatypes import PaginationResponse
from common.errors import ValidationError
from common.permissions import IsAuthenticated
from projects.config import settings
from projects.datatypes import PlanResponse, ProjectResponse
from projects.helpers import generate_token
from projects.repository import plan_repository, project_repository
from services.contract import Contract
from services.fusionauth import FusionAuthService
from services.node import TronNodeService
from strawberry.types import Info


@strawberry.type
class Query:
    @strawberry.field(permission_classes=[IsAuthenticated])
    async def projects(
        info: Info, limit: int = 20, offset: int = 0
    ) -> PaginationResponse[ProjectResponse]:
        projects, count = await project_repository.get_all(
            info.context.user.id, limit=limit, offset=offset
        )
        projects = ProjectResponse.from_dbs(projects)

        return PaginationResponse(
            list=projects,
            count=count,
            limit=limit,
            offset=offset,
        )

    @strawberry.field(permission_classes=[IsAuthenticated])
    async def project(info: Info, project_id: int) -> ProjectResponse:
        project = await project_repository.get_by_id(info.context.user.id, project_id)
        return ProjectResponse.from_db(project)

    @strawberry.field()
    async def plans() -> list[PlanResponse]:
        plans = await plan_repository.get_all(filters={"visibility": "public"})
        return [PlanResponse.from_db(row) for row in plans]


@strawberry.type
class Mutation:
    @strawberry.mutation(permission_classes=[IsAuthenticated])
    async def add_project(
        self, name: str, network_slug: str, info: Info
    ) -> ProjectResponse:
        if len(name) < 3:
            raise ValidationError("Name should be greater than 3 chars")

        plan = await plan_repository.get_by_slug(info.context.user.data.plan_slug)
        if not plan:
            plan = await plan_repository.get_by_slug("basic")
        assert plan, "Can not find plan"

        project = await project_repository.create(
            user_id=info.context.user.id,
            name=name,
            token=generate_token(),
            plan_id=plan.id,
            network_slug=network_slug,
        )
        return ProjectResponse.from_db(project)

    @strawberry.mutation(permission_classes=[IsAuthenticated])
    async def delete_project(self, project_id: int, info: Info) -> ProjectResponse:
        project = await project_repository.delete(info.context.user.id, project_id)
        return ProjectResponse.from_db(project)

    @strawberry.mutation(permission_classes=[IsAuthenticated])
    async def edit_project(
        self, project_id: int, name: str, info: Info
    ) -> ProjectResponse:
        if len(name) < 3:
            raise ValidationError("Name should be greater than 3 chars")

        project = await project_repository.update(
            info.context.user.id, project_id, name
        )
        return ProjectResponse.from_db(project)

    @strawberry.mutation(permission_classes=[IsAuthenticated])
    async def validate_payment(self, tx_hash: str, info: Info) -> bool:
        node_service = TronNodeService(
            settings.tron_node_url, settings.tron_node_api_key
        )
        async with node_service:
            data = await node_service.get_transaction_info(tx_hash)
            contract_address = data.get("contract_address")
            if not contract_address:
                return False

            contract_address = utils.to_base58(contract_address)
            if contract_address != settings.market_contract_address:
                return False

            logs = data.get("log", [])
            if not logs:
                return False

            abi = utils.load_abi("Market")["entrys"]
            contract = Contract(abi)

            for log in logs:
                if contract.can_decode(log):
                    event_name, params = contract.decode_log(log)
                    if (
                        event_name == "Payed"
                        and params["userId"] == info.context.user.id
                    ):
                        plan_slug = params["plan"]
                        await project_repository.set_plan_for_user_projects(
                            info.context.user.id, plan_slug
                        )

                        async with FusionAuthService(
                            settings.fusion_api_url,
                            settings.fusion_api_key,
                            settings.fusion_app_id,
                        ) as fusion:
                            data = {
                                "plan_slug": plan_slug,
                            }
                            await fusion.update_user_data(info.context.user.id, data)

                        return True

        return False
