import logging
import json
from typing import Optional

logger = logging.getLogger(__name__)

def format_message(msg: str) -> Optional[str]:
    if not msg:
        return None
    
    try:
        payload_data = {"data": msg}
        return json.dumps(payload_data, sort_keys=True)
    except (TypeError, ValueError) as e:
        logger.error(f"Failed to serialize message to JSON: {e}")
        return None
    