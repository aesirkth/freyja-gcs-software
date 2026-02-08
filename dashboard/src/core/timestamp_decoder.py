from datetime import datetime, timezone
from models.input_tm_data import TelemetryInput
from models.gcs_state import GCSState
import logging

logger = logging.getLogger(__name__)

def apply_unix_timestamp(received_timestamp: bytes, target_model: TelemetryInput | GCSState):
    try:
        ts_ms = int.from_bytes(received_timestamp, "little", signed=False)
        target_model.timestamp_ms = ts_ms
        timestamp = datetime.fromtimestamp(ts_ms/1000, tz=timezone.utc).strftime('%F %T.%f')[:-3]
        target_model.timestamp = timestamp
    except Exception as e:
        logger.exception(f"Error while decoding packet Unix timestamp. {e}")
       