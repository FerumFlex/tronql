from common.config import CommonSettings
from pydantic import Field


class Settings(CommonSettings):
    database_url: str = Field(env="database_url")
    redis_url: str = Field(env="redis_url")
    tron_node_url: str = Field(env="tron_node_url", default="https://api.trongrid.io/")
    tron_node_api_key: str = Field(env="tron_node_api_key", default=None)
    market_contract_address: str = Field(
        env="market_contract_address", default="TDH9dX6HxXcqBY5VRNF644b5Vdxh2EfvBm"
    )

    fusion_api_key: str = Field(env="fusion_api_key")
    fusion_api_url: str = Field(env="fusion_api_url")
    fusion_app_id: str = Field(env="fusion_app_id")


settings = Settings()
