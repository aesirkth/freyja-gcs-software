from src.core.cmd_transport import CommandTransport
from models.input_tm_data import TelemetryInput
from src.controller.test_cmd_controller import cmd_controller
from src.controller.board_decode_controller import decode_board_usb_frame
from src.controller.gse_decode_controller import decode_gse_usb_frame
from src.core.usb_frame_decoder import UsbFrameDecoder
from src.core.pkt_applier import PacketApplier
from models.gcs_state import GCSState
from src.state.tm_bus import tm_queue
from src.state.gse_bus import gse_queue
from src.state.system_state import gcs_state_history
from serial.tools import list_ports
from src.db.disk_saving import save_to_disk
import logging, asyncio
import serial

logger = logging.getLogger(__name__)

async def core_serial_task():
    ports = list_ports.comports()
    for port in ports:
        print(f"Device: {port.device}, Name: {port.name}, Description: {port.description}")
    board_ser_port = serial.Serial("/dev/cu.usbmodem1101", baudrate=9600, timeout=1)
    gse_ser_port = serial.Serial("", baudrate=9600, timeout=1)
    try:
        cmd_transporter = CommandTransport(gse_ser_port)
        usb_board_frame_decoder = UsbFrameDecoder(board_ser_port)
        usb_gse_frame_decoder = UsbFrameDecoder(gse_ser_port)
        pkt_applier = PacketApplier()

        latest_tel_data = TelemetryInput()
        latest_gcs_state = GCSState()
        latest_gse_data = GSEInput()
        while True:
            if decode_board_usb_frame(usb_board_frame_decoder, latest_tel_data, pkt_applier):
                if tm_queue.full():
                    _ = tm_queue.get_nowait()
            await tm_queue.put(latest_tel_data)
            await gcs_state_history.put(latest_gcs_state)
            save_to_disk(latest_tel_data)

            if decode_gse_usb_frame(usb_gse_frame_decoder, latest_gse_data, pkt_applier):
                if gse_queue.full():
                    _ = gse_queue.get_nowait()
            # await gse_queue.put()
            # save_to_disk()

            cmd_controller(cmd_transporter)

            await asyncio.sleep(0)
    except Exception as e:
        logger.error(f"Error while running core serial task. {e}")
    finally:
        board_ser_port.close()
        gse_ser_port.close()
