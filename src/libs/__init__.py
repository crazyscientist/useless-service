import asyncio
import random


async def delay(*, offset: float = 1, scale: float = 3) -> None:
    await asyncio.sleep(offset + random.random() * scale)
