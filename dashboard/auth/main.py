import sentry  # noqa
import strawberry
from auth.auth import router
from auth.config import settings
from auth.graphql import Mutation, Query
from common.context import get_user_context
from db.base import init_db
from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter

schema = strawberry.federation.Schema(
    query=Query, mutation=Mutation, enable_federation_2=True
)


graphql_app = GraphQLRouter(schema, context_getter=get_user_context)

app = FastAPI()
app.include_router(graphql_app, prefix="/graphql")
app.include_router(router)


@app.on_event("startup")
async def startup_event():
    await init_db(settings.database_url)
