import strawberry
from common.datatypes import PaginationResponse
from common.errors import ValidationError
from common.permissions import IsAuthenticated
from projects.datatypes import PlanResponse, ProjectResponse
from projects.helpers import generate_token
from projects.repository import plan_repository, project_repository
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
