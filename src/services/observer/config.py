from pydantic_settings import BaseSettings, SettingsConfigDict

from ...libs.config.amqp import AmqpConfig


class Config(BaseSettings):
    amqp: AmqpConfig = AmqpConfig()

    model_config = SettingsConfigDict(env_file=".env")


settings = Config()
