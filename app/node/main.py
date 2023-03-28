import sentry  # noqa
import strawberry
from fastapi import FastAPI
from node.context import get_custom_context
from node.graphql import Query
from strawberry.fastapi import GraphQLRouter

schema = strawberry.federation.Schema(query=Query, enable_federation_2=True)


graphql_app = GraphQLRouter(schema, context_getter=get_custom_context)

app = FastAPI()
app.include_router(graphql_app, prefix="/graphql")
