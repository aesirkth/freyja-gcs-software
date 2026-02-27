import logging
from src.core.usb_frame_decoder import UsbFrameDecoder
from models.proto import surtr_pb2

logger = logging.getLogger(__name__)

def decode_gse_usb_frame(decoder_service: UsbFrameDecoder, empty_gse_object: surtr_pb2.SurtrMessage) -> bool:
    try:
        usb_pkt_payload = decoder_service.read_gse_usb_frame()
        if not usb_pkt_payload:
            print("decoding error")
            return False
        empty_gse_object.ParseFromString(usb_pkt_payload)
        print(f"Switch1: {empty_gse_object.switch_states.sw1}")
        print(f"Switch2: {empty_gse_object.switch_states.sw2}")
        print(f"Switch3: {empty_gse_object.switch_states.sw3}")
        print(f"Switch4: {empty_gse_object.switch_states.sw4}")

        return True
    except Exception as e:
        logger.error(f"Error while reading and applying bytes to target object. {e}")
        return None
