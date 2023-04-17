import asyncio
import json
import pathlib

import pytest
from auth.config import settings as auth_settings
from auth.main import app as auth_app
from auth.main import startup as auth_startup
from db.base import Base, init_db
from httpx import AsyncClient
from networks.config import settings as networks_settings
from networks.main import app as networks_app
from networks.main import startup as networks_startup
from projects.config import settings as projects_settings
from projects.main import app as projects_app
from projects.main import startup as projects_startup
from stats.config import settings as stats_settings
from stats.main import app as stats_app
from stats.main import startup as stats_startup

FIXTURE_PATH = pathlib.Path(__file__).parent / "fixtures"


@pytest.fixture(scope="session")
def loop():
    return asyncio.get_event_loop()


def load_fixture(name, format="json"):
    with open(FIXTURE_PATH / name, mode="r") as f:
        if format == "json":
            return json.load(f)
        else:
            return f.read()


@pytest.fixture()
async def auth_client():
    async with AsyncClient(app=auth_app, base_url="http://test") as test_client:
        await auth_startup()
        yield test_client


@pytest.fixture
async def auth_config():
    return auth_settings


@pytest.fixture()
async def projects_client():
    async with AsyncClient(app=projects_app, base_url="http://test") as test_client:
        await projects_startup()
        yield test_client


@pytest.fixture
async def projects_config():
    return projects_settings


@pytest.fixture()
async def stats_client():
    async with AsyncClient(app=stats_app, base_url="http://test") as test_client:
        await stats_startup()
        yield test_client


@pytest.fixture
async def stats_config():
    return stats_settings


@pytest.fixture()
async def networks_client():
    async with AsyncClient(app=networks_app, base_url="http://test") as test_client:
        await networks_startup()
        yield test_client


@pytest.fixture
async def networks_config():
    return networks_settings


@pytest.fixture
async def db_engine(auth_config):
    engine = await init_db()
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    try:
        yield engine
    finally:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
