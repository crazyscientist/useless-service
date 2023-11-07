from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import AnyHttpUrl, RedisDsn

from .amqp import AmqpConfig


class Config(BaseSettings):
    amqp: AmqpConfig = AmqpConfig()
    base_url: AnyHttpUrl = "http://localhost:8000"
    redis: RedisDsn = "redis://localhost"

    model_config = SettingsConfigDict(env_file=".env")


settings = Config()
