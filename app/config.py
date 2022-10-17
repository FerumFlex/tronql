from pydantic import Field, BaseSettings


class Settings(BaseSettings):
    debug: bool = Field(env="debug", default=True)
    database_url: str = Field(env="database_url")
    kafka_url: str = Field(env="kafka_url")
    tron_node_url: str = Field(env="tron_node_url")

    sentry_dsn: str = Field(env="sentry_dsn", default=None)
    sentry_sample_rate: float = Field(env="sentry_sample_rate", default=0.05)
    environment: str = Field(env="environment", default="local")
    version: str = Field(env="version", default="local")
    microservice: str = Field(env="microservice", default="web")


settings = Settings()
