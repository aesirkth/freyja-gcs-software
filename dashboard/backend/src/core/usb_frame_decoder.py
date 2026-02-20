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
            b0 = self._read_exact(1)
            if not b0:
                print("error1")
                return False
            while True:
                if b0[0] == SURTR_SYNC_BYTE:
                    print("sync surtr")
                    return True
                elif b0[0] == SYNC0:
                    print("sync 1")
                    b1 = self._read_exact(1)
                    if not b1:
                        return False
                    if b1[0] == SYNC1:
                        return True
                    b0 = b1
                elif b0[0] == SYNC1:
                    b0 = self._read_exact(1)
                    print("sync 2")
                    if not b0:
                        return False
                else:
                    print("error2")
                    return False
        except Exception as e:
            logger.error(f"Error while looking for sync bytes. {e}")
            return None

    def _checksum(self, payload: bytes, crc_bytes: bytes) -> bool:
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
            if not self._find_sync_bytes():
                return None

            usb_pkt_timestamp = self._read_exact(8)
            if not usb_pkt_timestamp:
                return None
            
            header = self._read_exact(2)
            if not header:
                return None

            pkt_type_byte, pkt_len = header[0], header[1]
            if not (1 <= pkt_len <= 8):
                return None
            
            usb_pkt_payload = self._read_exact(pkt_len)
            if not usb_pkt_payload:
                return None
        
            usb_id = 0x700 + pkt_type_byte
            return usb_id, usb_pkt_timestamp, usb_pkt_payload
        except Exception as e:
            logger.error(f"Error while reading USB tm data frame. {e}")
            return None
        
    def read_gse_usb_frame(self) -> bytes:
        try:
            print("Decoding 1")
            if not self._find_sync_bytes():
                return None
            
            print("Decoding 2")
            pkt_len = self._read_exact(1)[0]
            if not (1 <= pkt_len <= 16):
                print("pkt len error")
                return None
            print(f"pkt_len: {pkt_len}")
           
            usb_pkt_payload = self._read_exact(pkt_len)
            if not usb_pkt_payload:
                return None
            print(f"pkt payload: {usb_pkt_payload}")
            crc_bytes = self._read_exact(4)
            checksum_result = self._checksum(usb_pkt_payload, crc_bytes)
            if checksum_result != True:
                print("checksum failed")
                return None
            
            return usb_pkt_payload
        except Exception as e:
            logger.error(f"Error while reading GSE USB frame. {e}")
            return None
