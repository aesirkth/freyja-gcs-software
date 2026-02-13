import serial, logging
from config.decoder_config import SYNC0, SYNC1, SURTR_SYNC_BYTE
from models.proto import surtr_pb2
import zlib

logger = logging.getLogger(__name__)

class UsbFrameDecoder:
    def __init__(self, ser_port: serial.Serial):
        self.ser = ser_port

    def _read_exact(self, n_bytes: int) -> bytes | None:
        buffer = b""
        while len(buffer) < n_bytes:
            chunk = self.ser.read(n_bytes - len(buffer))
            if not chunk:
                return None
            buffer += chunk
        return buffer

    def _find_sync_bytes(self) -> bool:
        try:
            b0 = self._read_exact(self.ser, 1)
            if not b0:
                return False
            while True:
                if b0[0] == SYNC0:
                    b1 = self._read_exact(self.ser, 1)
                    if not b1:
                        return False
                    if b1[0] == SYNC1:
                        return True
                    b0 = b1
                elif b0[0] == SURTR_SYNC_BYTE:
                    return True
                else:
                    b0 = self._read_exact(self.ser, 1)
                    if not b0:
                        return False
        except Exception as e:
            logger.error(f"Error while looking for sync bytes. {e}")
            return None
        
    def _checksum(payload: bytes, crc_bytes: bytes) -> bool:
        try:
            recv_crc = int.from_bytes(crc_bytes, "little")
            calc_crc = zlib.crc32(payload) & 0xFFFFFFFF

            if recv_crc != calc_crc:
                return None
            else:
                return True
        except Exception as e:
            logger.error(f"Error while computing checksum. {e}")
            return None

    def read_board_usb_frame(self):
        try:
            if not self._find_sync_bytes(self.ser):
                return None
        
            usb_pkt_timestamp = self._read_exact(self.ser, 8)
            if not usb_pkt_timestamp:
                return None
            
            header = self._read_exact(self.ser, 2)
            if not header:
                return None

            pkt_type_byte, pkt_len = header[0], header[1]
            if not (1 <= pkt_len <= 8):
                return None
            
            usb_pkt_payload = self._read_exact(self.ser, pkt_len)
            if not usb_pkt_payload:
                return None
        
            usb_id = 0x700 + pkt_type_byte
            return usb_id, usb_pkt_timestamp, usb_pkt_payload
        except Exception as e:
            logger.error(f"Error while reading USB tm data frame. {e}")
            return None
        
    def read_gse_usb_frame(self):
        try:
            if not self._find_sync_bytes(self.ser):
                return None
           
            pkt_len = self._read_exact(self.ser, 1)
            if not (1 <= pkt_len <= 8):
                return None
            
            usb_pkt_payload = self._read_exact(self.ser, pkt_len)
            if not usb_pkt_payload:
                return None

            crc_bytes = self._read_exact(self.ser, 4)
            checksum_result = self._checksum(usb_pkt_payload, crc_bytes)
            if checksum_result != True:
                return None
            
            return surtr_pb2.ParseFromString(usb_pkt_payload)
        except Exception as e:
            logger.error(f"Error while reading GSE USB frame. {e}")
            return None
