import asyncio
from src.core import core_serial_task
from ui.app import ui_task
import contextlib

async def main():
    tasks = [
        asyncio.create_task(core_serial_task(), name="core"),
    ]
    try:
        await ui_task()
    finally:
        for t in tasks:
            t.cancel()
        with contextlib.suppress(asyncio.CancelledError):
            await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main())
