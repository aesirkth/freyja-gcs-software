import asyncio

telemetry_queue = asyncio.LifoQueue(maxsize=300)
