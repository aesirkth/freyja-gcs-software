import asyncio
import contextlib
from src.core import core_loop
from ui.app import ui_loop

async def main():
    # start background producers
    tasks = [
        asyncio.create_task(core_loop(), name="core"),
        
    ]

    try:
        await ui_loop()
    finally:
        for t in tasks:
            t.cancel()
        with contextlib.suppress(asyncio.CancelledError):
            await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main())
