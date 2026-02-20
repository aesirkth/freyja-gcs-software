from models.proto import surtr_pb2
from src.core.cmd_transport import CommandTransport
from models.input_tm_data import TelemetryInput
from src.controller.test_cmd_controller import cmd_controller
from src.controller.board_decode_controller import decode_board_usb_frame
from src.controller.gse_decode_controller import decode_gse_usb_frame
from src.core.usb_frame_decoder import UsbFrameDecoder
from src.state.con_manager import ConnectionManager
from config.decoder_config import SURTR_BAUDRATE
from src.core.cmd_registry import CommandRegistry
from src.core.pkt_applier import PacketApplier
from src.state.cmd_queue import cmd_queue
from src.state.tm_bus import tm_queue
from src.state.gse_bus import gse_queue
from src.state.system_state import gcs_state_history
from src.db.disk_saving import save_to_disk
from src.utils.format_msg import format_message
from google.protobuf import json_format
from models.gcs_state import GCSState
from src.state.ports import port_list
from serial.tools import list_ports
import logging, asyncio
import serial
import json

logger = logging.getLogger(__name__)

async def core_serial_task(socket_manager: ConnectionManager):
    print("Running core serial task!")
    broadcasted = None
    ports = list_ports.comports()
    available_ports = []
    selected_ports = {"board": None, "gse": None}

    for port in ports:
        print(f"Device: {port.device}, Name: {port.name}, Description: {port.description}")
        available_ports.append(port.device)
   
    ports = {
        "ports": available_ports
    }
    """
    while selected_ports["board"] == None or selected_ports["gse"] == None:
        while len(socket_manager.active_connections) == 0:
            await asyncio.sleep(0)
        if broadcasted == None:
            await socket_manager.broadcast(json.dumps(ports))
            broadcasted = True
        if port_list:
            for port in port_list:
                if port["type"] == "board":
                    selected_ports["board"] = port["value"]
                else: 
                    selected_ports["gse"] = port["value"]
        await asyncio.sleep(0)
    """
    temp1 = "/dev/cu.usbmodem101"
    temp2 = "/dev/cu.usbserial-A505MMT7"
    # board_ser_port = serial.Serial("/dev/cu.usbmodem101", baudrate=9600, timeout=1)
    gse_ser_port = serial.Serial(temp2, baudrate=SURTR_BAUDRATE, timeout=1)

    try:
        cmd_transporter = CommandTransport(gse_ser_port)
        usb_gse_frame_decoder = UsbFrameDecoder(gse_ser_port)
        """
        usb_board_frame_decoder = UsbFrameDecoder(board_ser_port)
        pkt_applier = PacketApplier()
        """
        cmd_registry = CommandRegistry()
        latest_tel_data = TelemetryInput()
        latest_gcs_state = GCSState()
        latest_gse_data = surtr_pb2.SurtrMessage()
        while True:
            """
            if decode_board_usb_frame(usb_board_frame_decoder, latest_tel_data, latest_gcs_state, pkt_applier):
                if tm_queue.full():
                    _ = tm_queue.get_nowait()
            await tm_queue.put(latest_tel_data)
            await gcs_state_history.put(latest_gcs_state)
            save_to_disk(latest_tel_data)

            """
            if decode_gse_usb_frame(usb_gse_frame_decoder, latest_gse_data):
                if gse_queue.full():
                    _ = gse_queue.get_nowait()
            await gse_queue.put(latest_gse_data)
            # save_to_disk()

            await cmd_controller(cmd_transporter, cmd_registry)
            json_gse_data = json_format.MessageToJson(latest_gse_data)
            # gui_payload = format_message(key="adc" , value=json_gse_data)
            gui_payload = {
                "adc": json_gse_data
            }
            await socket_manager.broadcast(gui_payload)
            await socket_manager.broadcast("data_from_sensor")
            await asyncio.sleep(0)
    except Exception as e:
        logger.error(f"Error while running core serial task. {e}")
    finally:
        # board_ser_port.close()
        gse_ser_port.close()
