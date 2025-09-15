import asyncio, random
from models.input_data import TelemetryInput
from src.state.bus import telemetry_queue
import logging

logger = logging.getLogger(__name__)

async def core_serial_task():
    try:
        print("Running!")
        while True:
            # Temporary test data
            tel_data = TelemetryInput(
                speed=random.random()*50,
                battery_voltage=random.random()*50,
                tank_temp=random.random()*50,
            )
            print("Running")
            await telemetry_queue.put(tel_data)
            await asyncio.sleep(0.01) 
    except Exception as e:
        logger.error(f"Error while running core loop. {e}")
