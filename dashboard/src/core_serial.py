import logging, asyncio
from .core.can_conversion import read_and_apply_once
from models.input_tel_data import TelemetryInput
from src.state.bus import telemetry_queue
import serial

logger = logging.getLogger(__name__)

async def core_serial_task():
    ser = serial.Serial("/dev/cu.usbmodem112201", baudrate=9600, timeout=1)
    try:
        latest_tel_data = TelemetryInput()
        while True:
            if read_and_apply_once(ser, latest_tel_data):
                if telemetry_queue.full():
                    _ = telemetry_queue.get_nowait()
                await telemetry_queue.put(latest_tel_data)

            await asyncio.sleep(0)
    except Exception as e:
        logger.error(f"Error while running core serial task. {e}")
    finally:
        ser.close()
