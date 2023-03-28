from common.config import CommonSettings
from pydantic import Field


class Settings(CommonSettings):
    database_url: str = Field(env="database_url")
    redis_url: str = Field(env="redis_url")


settings = Settings()
