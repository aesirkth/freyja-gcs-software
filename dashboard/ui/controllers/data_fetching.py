from models.input_data import TelemetryInput
from src.state.bus import telemetry_queue
import logging

logger = logging.getLogger(__name__)

async def fetch_latest_tel_data() -> TelemetryInput:
    try:
        latest_tel_input = await telemetry_queue.get_nowait()

        if isinstance(latest_tel_input, TelemetryInput):
            return latest_tel_input
        else:
            raise TypeError
    except Exception as e:
        logger.error(f"Error while fetching latest telemetry data. {e}")
