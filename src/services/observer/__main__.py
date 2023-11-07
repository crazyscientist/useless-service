import asyncio

from .main import main, EVENT


try:
    asyncio.run(main())
except (KeyboardInterrupt, asyncio.CancelledError, SystemExit):
    EVENT.set()
