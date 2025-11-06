import logging, asyncio
from .core.can_conversion import read_next_frame_and_apply
from models.input_tel_data import TelemetryInput
from src.state.bus import telemetry_queue
from serial.tools import list_ports
from src.db.disk_saving import save_to_disk
import serial

logger = logging.getLogger(__name__)

async def core_serial_task():
    ports = list_ports.comports()
    for port in ports:
        print(f"Device: {port.device}, Name: {port.name}, Description: {port.description}")
    ser = serial.Serial("/dev/cu.usbmodem12101", baudrate=9600, timeout=1)
    try:
        latest_tel_data = TelemetryInput()
        while True:
            if read_next_frame_and_apply(ser, latest_tel_data):
                if telemetry_queue.full():
                    _ = telemetry_queue.get_nowait()
            await telemetry_queue.put(latest_tel_data)
            save_to_disk(latest_tel_data)

            await asyncio.sleep(0)
    except Exception as e:
        logger.error(f"Error while running core serial task. {e}")
    finally:
        ser.close()
