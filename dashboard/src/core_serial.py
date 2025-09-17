import logging, asyncio
import random
from .core.can_conversion import read_and_apply_once
from models.input_data import TelemetryInput
from src.state.bus import telemetry_queue
from serial.tools import list_ports
import serial

logger = logging.getLogger(__name__)

async def core_serial_task(port="/dev/ttyUSB0", baud=115200):
    ser = serial.Serial("/dev/cu.usbmodem112201", baudrate=9600, timeout=1)
    try:
        # ports = list_ports.comports()
        latest_tel_data = TelemetryInput()
        while True:
            if read_and_apply_once(ser, latest_tel_data):
                if telemetry_queue.full():
                    _ = telemetry_queue.get_nowait()
                await telemetry_queue.put(latest_tel_data)

            await asyncio.sleep(0)
            """
            tel_data = TelemetryInput(
                speed=random.random()*50,
                battery_voltage=random.random()*50,
                tank_temp=random.random()*50,
            )
            await telemetry_queue.put(tel_data)
            """
    except Exception as e:
        logger.error(f"Error while running core serial task. {e}")
    finally:
        ser.close()
