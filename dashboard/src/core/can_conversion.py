import serial, struct, logging
from .timestamp_decoder import apply_unix_timestamp
from models.input_tm_data import TelemetryInput
from .location_calc import calc_enu_location

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

def _find_sync_bytes(ser: serial.Serial) -> bool:
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

def _to_u8(pkt: bytes, byte_index: int):  return pkt[byte_index]
def _to_b1(pkt: bytes, byte_index: int):  return pkt[byte_index] != 0
def _to_f32(pkt: bytes, byte_index: int): return struct.unpack_from("<f", pkt, byte_index)[0]

def _apply_0x700(pkt: bytes, tel_object: TelemetryInput):
    tel_object.test_mode    = _to_b1(pkt, 0)
    print(f"Received GCS test mode pkt! Value: {tel_object.test_mode}")

def _apply_0x720(pkt: bytes, tel_object: TelemetryInput):
    tel_object.flight_state    = _to_u8(pkt, 0)
    tel_object.loki_state      = _to_u8(pkt, 1)
    tel_object.loki_substate   = _to_u8(pkt, 2)
    tel_object.drogue_deployed = _to_b1(pkt, 3)
    tel_object.main_deployed   = _to_b1(pkt, 4)
    tel_object.gnss_fix        = _to_b1(pkt, 5)

def _apply_0x721(pkt: bytes, tel_object: TelemetryInput):
    tel_object.fafnir_main_valve_pct = _to_f32(pkt, 0)
    tel_object.fafnir_sol_1 = _to_b1(pkt, 4)
    tel_object.fafnir_sol_2 = _to_b1(pkt, 5)
    tel_object.fafnir_sol_3 = _to_b1(pkt, 6)
    tel_object.fafnir_sol_4 = _to_b1(pkt, 7)

def _apply_0x722(pkt: bytes, tel_object: TelemetryInput): tel_object.thrust = _to_f32(pkt, 0)
def _apply_0x723(pkt: bytes, tel_object: TelemetryInput): tel_object.airbrake_safety = _to_b1(pkt, 0); tel_object.airbrake_pct = _to_f32(pkt, 1)
def _apply_0x724(pkt: bytes, tel_object: TelemetryInput): tel_object.pyro1 = _to_b1(pkt, 0); tel_object.pyro2 = _to_b1(pkt, 1); tel_object.pyro3 = _to_b1(pkt, 2)
def _apply_0x725(pkt: bytes, tel_object: TelemetryInput): tel_object.ax = _to_f32(pkt, 0); tel_object.ay = _to_f32(pkt, 4)
def _apply_0x726(pkt: bytes, tel_object: TelemetryInput): tel_object.az = _to_f32(pkt, 0)
def _apply_0x727(pkt: bytes, tel_object: TelemetryInput): tel_object.vx = _to_f32(pkt, 0); tel_object.vy = _to_f32(pkt, 4)
def _apply_0x72A(pkt: bytes, tel_object: TelemetryInput): tel_object.vz = _to_f32(pkt, 0)
def _apply_0x72B(pkt: bytes, tel_object: TelemetryInput): tel_object.roll = _to_f32(pkt, 0); tel_object.pitch = _to_f32(pkt, 4)
def _apply_0x72C(pkt: bytes, tel_object: TelemetryInput): tel_object.yaw = _to_f32(pkt, 0)

def _apply_0x72D(pkt: bytes, tel_object: TelemetryInput):
    tel_object.longitude = _to_f32(pkt, 0)
    tel_object.latitude  = _to_f32(pkt, 4)

    if getattr(tel_object, "launch_lat", None) is None:
        tel_object.launch_lon = tel_object.longitude
        tel_object.launch_lat = tel_object.latitude

    east, north, _ = calc_enu_location(
        lon=tel_object.longitude,
        lat=tel_object.latitude,
        launch_lon=tel_object.launch_lon,
        launch_lat=tel_object.launch_lat,
    )
    tel_object.east_enu = east
    tel_object.north_enu = north

def _apply_0x72E(pkt: bytes, tel_object: TelemetryInput): tel_object.altitude = _to_f32(pkt, 0)
def _apply_0x72F(pkt: bytes, tel_object: TelemetryInput): tel_object.sigurd_temp1 = _to_f32(pkt, 0); tel_object.sigurd_temp2 = _to_f32(pkt, 4)
def _apply_0x730(pkt: bytes, tel_object: TelemetryInput): tel_object.sigurd_temp3 = _to_f32(pkt, 0); tel_object.sigurd_temp4 = _to_f32(pkt, 4)
def _apply_0x731(pkt: bytes, tel_object: TelemetryInput): tel_object.fjalar_bat_voltage = _to_f32(pkt, 0); tel_object.loki_bat_voltage = _to_f32(pkt, 4)

DECODERS = {
    0x700: _apply_0x700,
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

def read_usb_frame(ser: serial.Serial):
    try:
        if not _find_sync_bytes(ser):
            return None
        
        can_pkt_timestamp = _read_exact(ser, 8)
        if not can_pkt_timestamp:
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
        return can_id, can_pkt_timestamp, can_pkt_payload
    except Exception as e:
        logger.error(f"Error while reading USB frame. {e}")
        return None

def read_next_frame_and_apply(ser: serial.Serial, empty_tel_object: TelemetryInput) -> bool:
    try:
        frame = read_usb_frame(ser)
        if not frame:
            return False
      
        can_id, can_pkt_timestamp, can_pkt_payload = frame
        if not can_id or not can_pkt_payload:
            return False

        decode_pkt = DECODERS.get(can_id)
        if decode_pkt:
            decode_pkt(can_pkt_payload, empty_tel_object)
            apply_unix_timestamp(can_pkt_timestamp, empty_tel_object)
            return True
        print("### Telemetry Object ### \n", empty_tel_object)
        return False
    except Exception as e:
        logger.error(f"Error while reading and applying bytes to telemetry object. {e}")
        return None
