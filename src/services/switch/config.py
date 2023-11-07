from pydantic import RedisDsn
from pydantic_settings import BaseSettings, SettingsConfigDict

from ...libs.config.amqp import AmqpConfig


class Config(BaseSettings):
    switches: list[str] = ["switch-1", "switch-2"]
    redis: RedisDsn = "redis://localhost"
    amqp: AmqpConfig = AmqpConfig()

    model_config = SettingsConfigDict(env_file=".env", env_nested_delimiter="__")


settings = Config()
