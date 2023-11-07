import asyncio

from ...libs.amqp import RoutingKey, subscribe
from ...libs.config import settings
from ...libs.models import AuditAction

from . import on_approval

EVENT = asyncio.Event()


async def _main():
    key = RoutingKey(switch="*", action=AuditAction.APPROVED)
    queue = await subscribe(settings=settings.amqp, routing_key=key)
    await queue.consume(callback=on_approval)
    await EVENT.wait()


try:
    asyncio.run(_main())
except (KeyboardInterrupt, asyncio.CancelledError, SystemExit):
    EVENT.set()
