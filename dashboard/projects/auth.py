import asyncio

import redis.asyncio as redis
import sentry  # noqa
from aiocache import Cache, cached
from db.base import init_db
from fastapi import FastAPI, Header, Request
from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse
from fastapi_limiter import FastAPILimiter
from fastapi_limiter.depends import RateLimiter
from projects.config import settings
from projects.models import Plan, Project
from projects.repository import project_repository
from stats.stats import Stats

app = FastAPI()
stats = Stats(settings.redis_url)


async def token_identifier(request: Request):
    token = request.headers.get("authorization")
    return f"token:{token}"


@app.on_event("startup")
async def startup_event():
    redis_limiter = redis.from_url(
        settings.redis_url, db=2, encoding="utf-8", decode_responses=True
    )

    await asyncio.gather(
        init_db(settings.database_url),
        FastAPILimiter.init(redis_limiter),
        stats.init(),
    )


@cached(ttl=10, cache=Cache.MEMORY)
async def get_project_plan_by_token(token: str) -> tuple[Project | None, Plan | None]:
    return await project_repository.get_project_plan_by_token(token)


@app.get("/")
@app.get("/{path}")
@app.get("/{path}/{path2}")
@app.get("/{path}/{path2}/{path3}")
@app.post("/")
@app.post("/{path}")
@app.post("/{path}/{path2}")
@app.post("/{path}/{path2}/{path3}")
async def auth(
    request: Request,
    authorization: str | None = Header(default=None),
    tron_pro_api_key: str | None = Header(default=None),
):
    access_token = authorization or tron_pro_api_key
    if not access_token:
        raise HTTPException(status_code=401, detail="auth token is not set")

    project, plan = await get_project_plan_by_token(access_token)
    if not project:
        raise HTTPException(status_code=403, detail="wrong auth token")
    if not plan:
        raise HTTPException(status_code=500, detail="plan for project does not exist")

    limiter = RateLimiter(
        times=plan.rate_limit, seconds=plan.rate_period, identifier=token_identifier
    )
    response = JSONResponse({"status": "ok"})

    # will raise exception incase of limit reached
    await limiter(request, response)

    await stats.track(project.user_id, project.id)

    return response
