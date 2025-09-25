import pymap3d as pm
import logging

logger = logging.getLogger(__name__)

def calc_location(lat: float, lon: float, launch_lat: float, launch_lon: float) -> tuple:
    try:
        return pm.geodetic2enu(lat=lat, lon=lon, h=0.0, lat0=launch_lat, lon0=launch_lon, h0=0.0, deg=True)
    except Exception as e:
        logger.error(f"Error while calculating ENU location. {e}")
        raise
