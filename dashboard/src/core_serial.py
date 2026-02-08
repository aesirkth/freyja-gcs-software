import logging, asyncio
from .core.can_conversion import read_next_frame_and_apply
from src.controller.test_cmd_controller import cmd_controller
from src.core.cmd_transport import CommandTransport
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
    board_ser = serial.Serial("/dev/cu.usbmodem1101", baudrate=9600, timeout=1)
    gse_ser = serial.Serial("", baudrate=9600, timeout=1)
    try:
        cmd_transporter = CommandTransport(gse_ser)
        latest_tel_data = TelemetryInput()
        latest_gcs_state = GCSState()
        while True:
            # Apply the same for GSE inputs
            if read_next_frame_and_apply(board_ser, latest_tel_data, latest_gcs_state):
                if tm_queue.full():
                    _ = tm_queue.get_nowait()
            await tm_queue.put(latest_tel_data)
            await gcs_state_history.put(latest_gcs_state)
            save_to_disk(latest_tel_data)

            if read_next_frame_and_apply(gse_ser, latest_tel_data):
                if tm_queue.full():
                    _ = tm_queue.get_nowait()
            # Why await?
            # await tm_queue.put(latest_tel_data)
            cmd_controller(cmd_transporter)

            await asyncio.sleep(0)
    except Exception as e:
        logger.error(f"Error while running core serial task. {e}")
    finally:
        board_ser.close()
        gse_ser.close()
