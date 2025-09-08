from models.input_data import TelemetryInput
from src.state.bus import telemetry_queue
import logging

logger = logging.getLogger(__name__)

def fetch_latest_tel_data():
    try:
        if isinstance(telemetry_queue, TelemetryInput):
            return telemetry_queue
        else:
            raise TypeError
    except Exception as e:
        logger.e(f"Error while fetching lates telemetry data. {e}")
