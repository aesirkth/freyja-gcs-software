import asyncio, random, logging
from src.core.location_calc import calc_enu_location
from models.input_tm_data import TelemetryInput
from src.state.tm_bus import tm_queue

logger = logging.getLogger(__name__)

async def fetch_latest_tel_data() -> TelemetryInput:
    try:
        latest_tel_input = tm_queue.get_nowait()
    except asyncio.QueueEmpty:
        tm_queue.put_nowait(TelemetryInput())
        latest_tel_input = tm_queue.get_nowait()
    try:
        if isinstance(latest_tel_input, TelemetryInput):
            test_lat = 59.334591 + random.random() / 100
            test_lon = 18.063240 + random.random() / 100
            east, north, _ = calc_enu_location(
                lon=test_lon,
                lat=test_lat,
                launch_lon=18.063240,
                launch_lat=59.334591,
            )
            latest_tel_input.east_enu = 18.063240 + random.random() / 10
            latest_tel_input.north_enu = 18.063240 + random.random() / 10
            # print(east, north)
            # print(latest_tel_input)
            return latest_tel_input
        else:
            print("wrong type")
            raise TypeError
    except Exception as e:
        logger.exception(f"Error while fetching latest telemetry data. {e}")
