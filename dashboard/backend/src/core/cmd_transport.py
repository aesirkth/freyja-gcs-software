import logging
from config.decoder_config import SURTR_SYNC_BYTE, SURTR_CRC_POLY, SURTR_CRC_SEED
import zlib

logger = logging.getLogger(__name__)

class CommandTransport:
    def __init__(self, serial_port):
        self._serial = serial_port
    
    def crc16(poly, seed, buf):
        crc = seed
        for byte in buf:
            crc ^= (byte << 8)
            for _ in range(8):
                if crc & 0x8000:
                    crc = (crc << 1) ^ poly
                else:
                    crc = crc << 1
        return crc & 0xFFFF	

    def write(self, protobuf_message) -> int:
        try:
            payload = protobuf_message.SerializeToString()
            payload_len = len(payload)

            if payload_len > 255:
                raise ValueError(f"Payload too large for 1-byte length: {payload_len} bytes")

            packet = bytes([SURTR_SYNC_BYTE, payload_len]) + payload
            crc_value = self.crc16(SURTR_CRC_POLY, SURTR_CRC_SEED, packet)
            frame = packet + crc_value.to_bytes(2, "little")

            return self._serial.write(frame)

        except Exception as e:
            logger.exception(f"Error while writing data over USB. {e}")
            return 0

    def save_to_disk(self):
        pass
