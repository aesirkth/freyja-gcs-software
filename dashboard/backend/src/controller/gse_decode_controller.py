import logging
from src.core.usb_frame_decoder import UsbFrameDecoder
from models.proto import surtr_pb2

logger = logging.getLogger(__name__)

def decode_gse_usb_frame(decoder_service: UsbFrameDecoder, empty_gse_object: surtr_pb2.SurtrMessage) -> bool:
    try:
        usb_pkt_payload = decoder_service.read_gse_usb_frame()
        if not usb_pkt_payload:
            return False

        empty_gse_object.ParseFromString(usb_pkt_payload)
        return True
    except Exception as e:
        logger.error(f"Error while reading and applying bytes to target object. {e}")
        return None
   