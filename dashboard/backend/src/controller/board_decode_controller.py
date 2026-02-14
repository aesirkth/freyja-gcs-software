import logging
from src.core.usb_frame_decoder import UsbFrameDecoder
from models.input_tm_data import TelemetryInput
from src.core.timestamp_decoder import apply_unix_timestamp
from src.core.pkt_applier import PacketApplier
from models.gcs_state import GCSState

logger = logging.getLogger(__name__)

def decode_board_usb_frame(decoder_service: UsbFrameDecoder, empty_tel_object: TelemetryInput, empty_gcs_state_object: GCSState, pkt_applier: PacketApplier) -> bool:
    try:
        frame = decoder_service.read_board_usb_frame()
        if not frame:
            return False
     
        usb_id, usb_pkt_timestamp, usb_pkt_payload = frame
        if not usb_id or not usb_pkt_payload:
            return False

        if pkt_applier:
            if usb_id == 0x700:
                pkt_applier.apply(usb_id, usb_pkt_payload, empty_gcs_state_object)
                apply_unix_timestamp(usb_pkt_timestamp, empty_gcs_state_object)
            else:
                pkt_applier.apply(usb_id, usb_pkt_payload, empty_tel_object)
                apply_unix_timestamp(usb_pkt_timestamp, empty_tel_object)
            return True
       
        return False
    except Exception as e:
        logger.error(f"Error while reading and applying bytes to target object. {e}")
        return None