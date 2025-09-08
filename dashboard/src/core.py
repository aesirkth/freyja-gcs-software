import asyncio, random
from dashboard.models.input_data import TelemetryInput
from state.bus import telemetry_q
import logging

logger = logging.getLogger(__name__)

async def core_loop():
    try:
        while True:
            tel = TelemetryInput(
                speed=20 + random.random()*5,
                battery_voltage=12.1,
                tank_temp=35.0,
            )
            if telemetry_q.full():
                _ = telemetry_q.get_nowait()
            await telemetry_q.put(tel)
            await asyncio.sleep(0.01) 
    except Exception as e:
        logger.e(f"Error while running core loop. {e}")
