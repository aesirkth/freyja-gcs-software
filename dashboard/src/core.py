import asyncio, random
from models.input_data import TelemetryInput
from src.state.bus import telemetry_queue
import logging

logger = logging.getLogger(__name__)

async def core_loop():
    try:
        while True:
            # Temporary test data
            tel = TelemetryInput(
                speed=20 + random.random()*5,
                battery_voltage=12.1,
                tank_temp=35.0,
            )
            await telemetry_queue.put(tel)
            await asyncio.sleep(0.01) 
    except Exception as e:
        logger.error(f"Error while running core loop. {e}")
