import asyncio, serial
from .core.can_conversion import read_and_apply_once
from models.input_data import TelemetryInput
from src.state.bus import telemetry_queue
import logging

logger = logging.getLogger(__name__)

async def core_serial_task(port="/dev/ttyUSB0", baud=115200):
    try:    
        ser = serial.Serial(port, baudrate=baud, timeout=0.2)
        latest_tel_data = TelemetryInput()
        while True:
            if read_and_apply_once(ser, latest_tel_data):
                if telemetry_queue.full():
                    _ = telemetry_queue.get_nowait()
                await telemetry_queue.put(latest_tel_data)
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
