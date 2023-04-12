import sentry  # noqa
import strawberry
from common.context import get_user_context
from db.base import init_db
from db.helpers import health_check
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from projects.config import settings
from projects.graphql import Mutation, Query
from strawberry.fastapi import GraphQLRouter

schema = strawberry.federation.Schema(
    query=Query, mutation=Mutation, enable_federation_2=True
)


graphql_app = GraphQLRouter(schema, context_getter=get_user_context)

app = FastAPI()
app.include_router(graphql_app, prefix="/graphql")


@app.on_event("startup")
async def startup():
    await init_db(settings.database_url)


@app.get("/health")
async def health_check_endpoint():
    result = await health_check()
    return JSONResponse(
        {"status": "ok" if result else "error"},
        status_code=200 if result else 500,
    )
