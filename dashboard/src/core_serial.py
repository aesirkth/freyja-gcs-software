import logging, asyncio
from .core.can_conversion import read_next_frame_and_apply
from models.input_tm_data import TelemetryInput
from models.gcs_state import GCSState
from src.state.tm_bus import tm_queue
from src.state.system_state import gcs_state_history
from serial.tools import list_ports
from src.db.disk_saving import save_to_disk
import serial

logger = logging.getLogger(__name__)

async def core_serial_task():
    ports = list_ports.comports()
    for port in ports:
        print(f"Device: {port.device}, Name: {port.name}, Description: {port.description}")
    ser = serial.Serial("/dev/cu.usbmodem1101", baudrate=9600, timeout=1)
    try:
        latest_tel_data = TelemetryInput()
        latest_gcs_state = GCSState()
        while True:
            if read_next_frame_and_apply(ser, latest_tel_data, latest_gcs_state):
                if tm_queue.full():
                    _ = tm_queue.get_nowait()
            await tm_queue.put(latest_tel_data)
            await gcs_state_history.put(latest_gcs_state)
            save_to_disk(latest_tel_data)

            await asyncio.sleep(0)
    except Exception as e:
        logger.error(f"Error while running core serial task. {e}")
    finally:
        ser.close()
