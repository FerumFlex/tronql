from pydantic import BaseSettings, Field


class CommonSettings(BaseSettings):
    debug: bool = Field(env="debug", default=True)

    sentry_dsn: str = Field(env="sentry_dsn", default=None)
    sentry_sample_rate: float = Field(env="sentry_sample_rate", default=0.05)
    environment: str = Field(env="environment", default="local")
    version: str = Field(env="version", default="local")
    microservice: str = Field(env="microservice", default="web")
