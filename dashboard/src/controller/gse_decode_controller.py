import logging
from src.core.usb_frame_decoder import UsbFrameDecoder
from src.core.pkt_applier import PacketApplier

logger = logging.getLogger(__name__)

def decode_gse_usb_frame(decoder_service: UsbFrameDecoder, empty_gse_object: GSEInput, pkt_applier: PacketApplier) -> bool:
    try:
        usb_pkt_payload = decoder_service.read_gse_usb_frame
        if not pkt_payload:
            return False
    
        decode_pkt = DECODERS.get(usb_id)
        if decode_pkt:
            if usb_id == 0x700:
                decode_pkt(usb_pkt_payload, empty_gse_object)
                apply_unix_timestamp(usb_pkt_timestamp, empty_gse_object)
            
            return True
       
        return False
    except Exception as e:
        logger.error(f"Error while reading and applying bytes to target object. {e}")
        return None