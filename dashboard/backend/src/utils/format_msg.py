import logging
import json
from typing import Optional

logger = logging.getLogger(__name__)

def format_message(value: str, key: str="data") -> Optional[str]:
    if not value:
        return None
    try:
        payload_data = {key: value}
        return json.dumps(payload_data, sort_keys=True)
    except (TypeError, ValueError) as e:
        logger.error(f"Failed to serialize message to JSON: {e}")
        return None
    