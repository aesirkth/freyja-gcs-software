import logging

logger = logging.getLogger(__name__)

def fmt_bool(val: bool) -> str:
    try:
        if val is True:  return "Yes"
        if val is False: return "No"

        return "--"
    except Exception as e: 
        logger.error(f"Error while formatting bool value. {e}")
