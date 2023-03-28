import sentry_sdk
from config import settings
from logger import logger
from sentry_sdk.integrations.fastapi import FastApiIntegration
from sentry_sdk.integrations.sqlalchemy import SqlalchemyIntegration
from sentry_sdk.integrations.starlette import StarletteIntegration

if settings.sentry_dsn:
    sentry_sdk.init(
        dsn=settings.sentry_dsn,
        integrations=[
            SqlalchemyIntegration(),
            FastApiIntegration(),
            StarletteIntegration(),
        ],
        traces_sample_rate=settings.sentry_sample_rate,
        environment=settings.environment,
        release=settings.version,
    )
    sentry_sdk.set_tag("microservice", settings.microservice)

    logger.info("🚀 Sentry initialized 🚀")
