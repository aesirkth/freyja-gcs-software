import asyncio

gcs_state_history = asyncio.LifoQueue(maxsize=1000)
