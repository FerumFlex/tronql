import sqlalchemy as sa
from db.helpers import get_count, get_scalar, get_scalars
from db.utils import session_manager
from projects.models import Plan, Project


class ProjectRepository:
    async def _get_by_id(self, user_id: str, object_id: int) -> Project | None:
        query = (
            sa.select(Project)
            .where(Project.user_id == user_id)
            .where(Project.id == object_id)
            .order_by(Project.created_at.desc())
        )
        return await get_scalar(query)

    async def get_all(
        self, user_id: str, limit: int, offset: int
    ) -> tuple[list[Project], int]:
        async with session_manager():
            query = (
                sa.select(Project)
                .where(Project.user_id == user_id)
                .order_by(Project.created_at.desc())
            )

            count = await get_count(query)
            projects = await get_scalars(query, limit=limit, offset=offset)

            return (projects, count)

    async def get_by_id(self, user_id: str, object_id: int) -> Project:
        async with session_manager():
            project = await self._get_by_id(user_id, object_id)
            assert project, "Project is not find"
            return project

    async def create(
        self, user_id: str, plan_id: int, name: str, token: str, network_slug: str
    ) -> Project:
        async with session_manager():
            data = {
                "name": name,
                "user_id": user_id,
                "token": token,
                "plan_id": plan_id,
                "network_slug": network_slug,
            }
            project = await Project.create(**data)
            return project

    async def delete(self, user_id: str, object_id: int) -> Project:
        async with session_manager():
            project = await self._get_by_id(user_id, object_id)
            assert project, "Project is not find"
            await project.delete()
            return project

    async def update(self, user_id: str, object_id: int, name: str) -> Project:
        async with session_manager():
            project = await self._get_by_id(user_id, object_id)
            assert project, "Project is not find"
            await project.update(name=name)
            return project

    async def get_project_plan_by_token(
        self, token: str
    ) -> tuple[Project | None, Plan | None]:
        async with session_manager() as session:
            query = (
                sa.select(Project, Plan)
                .join(Plan, Project.plan_id == Plan.id)
                .where(Project.token == token)
            )
            result = await session.execute(query)
            data = result.mappings().one_or_none()
            return (data.get("Project"), data.get("Plan")) if data else (None, None)

    async def set_plan_for_user_projects(self, user_id: str, plan_slug: str) -> None:
        plan = await plan_repository.get_by_slug(plan_slug)
        async with session_manager() as session:
            query = (
                sa.update(Project)
                .values(plan_id=plan.id)
                .where(Project.user_id == user_id)
            )
            await session.execute(query)


class PlanRepository:
    async def get_by_ids(self, plan_ids: list[int]) -> list[Plan]:
        async with session_manager():
            query = sa.select(Plan).where(Plan.id.in_(plan_ids))
            return await get_scalars(query)

    async def get_all(self, filters: dict[str, any] | None = None) -> list[Plan]:
        async with session_manager():
            query = sa.select(Plan).order_by(Plan.requests_per_month.asc())
            if filters:
                for key, value in filters.items():
                    column = getattr(Plan, key)
                    query = query.where(column == value)
            return await get_scalars(query)

    async def get_by_slug(self, slug: str) -> list[Plan]:
        async with session_manager():
            query = sa.select(Plan).where(Plan.slug == slug)
            return await get_scalar(query)


project_repository = ProjectRepository()
plan_repository = PlanRepository()
