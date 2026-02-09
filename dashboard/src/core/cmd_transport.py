import logging
import zlib

logger = logging.getLogger(__name__)

# Hämta från config fil istället
MAGIC = b"\xAA\xAA"

class CommandTransport:
    def __init__(self, serial_port):
        self._serial = serial_port

    def write(self, protobuf_message) -> int:
        try:
            payload = protobuf_message.SerializeToString()
            payload_len = len(payload)

            if payload_len > 0xFFFF:
                raise ValueError(f"Payload too large for uint16 length: {payload_len} bytes")

            length_bytes = payload_len.to_bytes(2, "little")

            crc = zlib.crc32(payload) & 0xFFFFFFFF
            crc_bytes = crc.to_bytes(4, "little")

            frame = MAGIC + length_bytes + payload + crc_bytes

            return self._serial.write(frame)

        except Exception:
            logger.exception("Error while writing data over USB")
            return 0

    def save_to_disk(self):
        pass
