import logging

logger = logging.getLogger(__name__)

def format_value(value, unit, digits=1):
    try:
        if value is None:
            return f"-- {unit}"
        if isinstance(value, float):
            return f"{value:.{digits}f} {unit}"
        return f"{value} {unit}"
    except Exception as e:
        logger.error(f"Error while formatting value for dashboard. {e}")
