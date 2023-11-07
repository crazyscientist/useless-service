import asyncio

from ...libs.amqp import RoutingKey, subscribe
from ...libs.config import settings
from . import on_action


EVENT = asyncio.Event()


async def _main():
    key = RoutingKey(switch="*", action="*")
    queue = await subscribe(settings=settings.amqp, routing_key=key)
    await queue.consume(callback=on_action)
    await EVENT.wait()


try:
    asyncio.run(_main())
except (KeyboardInterrupt, asyncio.CancelledError, SystemExit):
    EVENT.set()
