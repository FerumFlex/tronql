from common.config import CommonSettings
from pydantic import Field


class Settings(CommonSettings):
    database_url: str = Field(env="database_url")
    redis_url: str = Field(env="redis_url")

    fusion_api_key: str = Field(env="fusion_api_key")
    fusion_api_url: str = Field(env="fusion_api_url")
    fusion_app_id: str = Field(env="fusion_app_id")


settings = Settings()
