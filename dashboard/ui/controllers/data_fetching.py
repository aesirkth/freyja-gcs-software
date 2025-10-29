import random
from src.core.location_calc import calc_enu_location
from models.input_tel_data import TelemetryInput
from src.state.bus import telemetry_queue
import logging

logger = logging.getLogger(__name__)

async def fetch_latest_tel_data() -> TelemetryInput:
    latest_tel_input: TelemetryInput = await telemetry_queue.get()
    print("Value: ", latest_tel_input)
    try:
        if isinstance(latest_tel_input, TelemetryInput):
            test_lat = 59.334591 + random.random() / 10
            test_lon = 18.063240 + random.random() / 10
            east, north, _ = calc_enu_location(
                lon=test_lon,
                lat=test_lat,
                launch_lon=18.063240,
                launch_lat=59.334591,
            )
            latest_tel_input.east_enu = east
            latest_tel_input.north_enu = north
             
            return latest_tel_input
        else:
            print("wrong type")
            raise TypeError
    except Exception as e:
        logger.exception(f"Error while fetching latest telemetry data. {e}")
