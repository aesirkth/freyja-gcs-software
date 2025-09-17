from models.input_tel_data import TelemetryInput
import logging

logger = logging.getLogger(__name__)

async def save_to_disk(data: TelemetryInput) -> bool:
    try:
        return
    except Exception as e:
        logger.error(f"Error while saving telemetry data to persistent disk storage. {e}")
