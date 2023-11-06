from dataclasses import dataclass
from threading import local

from aio_pika.abc import AbstractQueue, AbstractChannel, AbstractExchange
from aio_pika import connect_robust, Connection, ExchangeType, Message
from pydantic import BaseModel

from .config.amqp import AmqpConfig


THREAD_LOCAL = local()
CONN_NAME = "connection"
EXCHANGE_OPTS = {
    "type": ExchangeType.TOPIC,
    "durable": True,
    "auto_delete": False
}


@dataclass
class RoutingKey:
    switch: str
    action: str
    prefix: str = "useless"

    def __str__(self):
        return f"{self.prefix}.{self.switch}.{self.action}"


async def connect(settings: AmqpConfig) -> Connection:
    connection = getattr(THREAD_LOCAL, CONN_NAME, None)
    if connection is None:
        connection = await connect_robust(url=str(settings.dsn))
        setattr(THREAD_LOCAL, CONN_NAME, connection)

    return connection


async def declare_exchange(channel: AbstractChannel, settings: AmqpConfig) -> AbstractExchange:
    opts = EXCHANGE_OPTS.copy()
    opts["name"] = settings.exchange
    exchange = await channel.declare_exchange(**opts)
    return exchange


async def publish(settings: AmqpConfig, routing_key: RoutingKey, message: BaseModel) -> None:
    connection = await connect(settings=settings)
    channel = await connection.channel()
    exchange = await declare_exchange(channel=channel, settings=settings)
    await exchange.publish(message=Message(body=message.model_dump_json().encode(),
                                           content_type="text/json"),
                           routing_key=str(routing_key))


async def subscribe(settings: AmqpConfig, routing_key: RoutingKey) -> AbstractQueue:
    connection = await connect(settings=settings)
    channel = await connection.channel()
    exchange = await declare_exchange(channel=channel, settings=settings)
    queue = await channel.declare_queue(exclusive=True)
    await queue.bind(exchange=exchange, routing_key=str(routing_key))
    return queue
