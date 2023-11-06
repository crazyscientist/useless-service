from pydantic import AmqpDsn
from pydantic_settings import BaseSettings


class AmqpConfig(BaseSettings):
    dsn: AmqpDsn = "amqp://guest@localhost:5672/"
    exchange: str = "useless-exchange"
