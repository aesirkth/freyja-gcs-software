import serial, struct
from dashboard.models.input_data import TelemetryInput
import logging

logger = logging.getLogger(__name__)

SYNC0 = 0xAA
SYNC1 = 0xAA

def _read_exact(ser: serial.Serial, n_bytes: int) -> bytes | None:
    buffer = b""
    while len(buffer) < n_bytes:
        chunk = ser.read(n_bytes - len(buffer))
        if not chunk:
            return None
        buffer += chunk
    return buffer

def _find_sync(ser: serial.Serial) -> bool:
    b0 = _read_exact(ser, 1)
    if not b0:
        return False
    while True:
        if b0[0] == SYNC0:
            b1 = _read_exact(ser, 1)
            if not b1:
                return False
            if b1[0] == SYNC1:
                return True
            b0 = b1
        else:
            b0 = _read_exact(ser, 1)
            if not b0:
                return False

def _u8(b, byte_index):  return b[byte_index]
def _b1(b, byte_index):  return b[byte_index] != 0
def _f32(b, byte_index): return struct.unpack_from("<f", b, byte_index)[0]  # Assuming STM32 little-endian?

def _apply_0x720(p, t):
    t.flight_state    = _u8(p, 0)
    t.loki_state      = _u8(p, 1)
    t.loki_substate   = _u8(p, 2)
    t.drogue_deployed = _b1(p, 3)
    t.main_deployed   = _b1(p, 4)
    t.gnss_fix        = _b1(p, 5)

def _apply_0x721(p, t):
    t.fafnir_main_valve_pct = _f32(p, 0)
    t.fafnir_sol_1 = _b1(p, 4)
    t.fafnir_sol_2 = _b1(p, 5)
    t.fafnir_sol_3 = _b1(p, 6)
    t.fafnir_sol_4 = _b1(p, 7)

def _apply_0x722(pkt, tel_object): tel_object.thrust = _f32(pkt, 0)
def _apply_0x723(pkt, tel_object): tel_object.airbrake_safety = _b1(pkt, 0); tel_object.airbrake_pct = _f32(pkt, 1)
def _apply_0x724(pkt, tel_object): tel_object.pyro1 = _b1(pkt, 0); tel_object.pyro2 = _b1(pkt, 1); tel_object.pyro3 = _b1(pkt, 2)
def _apply_0x725(pkt, tel_object): tel_object.ax = _f32(pkt, 0); tel_object.ay = _f32(pkt, 4)
def _apply_0x726(pkt, tel_object): tel_object.az = _f32(pkt, 0)
def _apply_0x727(pkt, tel_object): tel_object.vx = _f32(pkt, 0); tel_object.vy = _f32(pkt, 4)
def _apply_0x72A(pkt, tel_object): tel_object.vz = _f32(pkt, 0)
def _apply_0x72B(pkt, tel_object): tel_object.roll = _f32(pkt, 0); tel_object.pitch = _f32(pkt, 4)
def _apply_0x72C(pkt, tel_object): tel_object.yaw = _f32(pkt, 0)
def _apply_0x72D(pkt, tel_object): tel_object.longitude = _f32(pkt, 0); tel_object.latitude = _f32(pkt, 4)
def _apply_0x72E(pkt, tel_object): tel_object.altitude = _f32(pkt, 0)
def _apply_0x72F(pkt, tel_object): tel_object.sigurd_temp1 = _f32(pkt, 0); tel_object.sigurd_temp2 = _f32(pkt, 4)
def _apply_0x730(pkt, tel_object): tel_object.sigurd_temp3 = _f32(pkt, 0); tel_object.sigurd_temp4 = _f32(pkt, 4)
def _apply_0x731(pkt, tel_object): tel_object.fjalar_bat_voltage = _f32(pkt, 0); tel_object.loki_bat_voltage = _f32(pkt, 4)

DECODERS = {
    0x720: _apply_0x720,
    0x721: _apply_0x721,
    0x722: _apply_0x722,
    0x723: _apply_0x723,
    0x724: _apply_0x724,
    0x725: _apply_0x725,
    0x726: _apply_0x726,
    0x727: _apply_0x727,
    0x72A: _apply_0x72A,
    0x72B: _apply_0x72B,
    0x72C: _apply_0x72C,
    0x72D: _apply_0x72D,
    0x72E: _apply_0x72E,
    0x72F: _apply_0x72F,
    0x730: _apply_0x730,
    0x731: _apply_0x731,
}

def read_packet_blocking(ser: serial.Serial):
    if not _find_sync(ser):
        return None
    header = _read_exact(ser, 2)
    if not header:
        return None
    pkt_type_byte, pkt_len = header[0], header[1]
    if not (1 <= pkt_len <= 8):
        return None
    can_pkt_payload = _read_exact(ser, pkt_len)
    if not can_pkt_payload:
        return None
    can_id = 0x700 + pkt_type_byte

    return can_id, can_pkt_payload

def read_and_apply_once(ser: serial.Serial, empty_tel_object: TelemetryInput) -> bool:
    can_id, can_pkt_payload = read_packet_blocking(ser)

    if not can_id or not can_pkt_payload:
        return False
    decode_pkt = DECODERS.get(can_id)

    if decode_pkt:
        decode_pkt(can_pkt_payload, empty_tel_object)
        return True
    return False
