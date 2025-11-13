from datetime import datetime, timezone
from models.input_tel_data import TelemetryInput
import logging

logger = logging.getLogger(__name__)

def apply_unix_timestamp(received_timestamp: bytes, tel_object: TelemetryInput):
    try:
        ts_ms = int.from_bytes(received_timestamp, "little", signed=False)
        tel_object.timestamp_ms = ts_ms
        timestamp = datetime.fromtimestamp(ts_ms/1000, tz=timezone.utc).strftime('%F %T.%f')[:-3]
        tel_object.timestamp = timestamp
    except Exception as e:
        logger.exception(f"Error while decoding packet Unix timestamp. {e}")
        