import logging
import json

logger = logging.getLogger(__name__)

def format_message(msg: str):
    try:
        formatted = json.dumps(msg)
    except Exception as e:
        logger.error(f"Error when formatting message. {e}")