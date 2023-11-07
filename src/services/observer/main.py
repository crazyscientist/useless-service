import asyncio

from ...libs.amqp import subscribe, RoutingKey
from ...libs.config import settings
from ...libs.models import AuditAction

from . import on_change


EVENT = asyncio.Event()


async def main():
    key = RoutingKey(switch="*", action=AuditAction.CHANGED)
    queue = await subscribe(settings=settings.amqp, routing_key=key)
    await queue.consume(callback=on_change)
    await EVENT.wait()
