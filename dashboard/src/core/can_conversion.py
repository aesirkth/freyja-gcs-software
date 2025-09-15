import serial, struct
from dashboard.models.input_data import TelemetryInput

FMT = {
    20: "<BBB??",  # state: flight,u8; loki,u8; sub,u8; drogue,bool; gnss,bool
    21: "<f????",  # fafnir: main_valve_pct,f32; 4x bool
    22: "<f",      # thrust
    23: "<?f",     # airbrake: safety,bool; pct,f32
    24: "<???",    # pyro: 3x bool
    25: "<ff",     # acc_1: ax, ay
    26: "<f",      # acc_2: az
    27: "<ff",     # vel_1: vx, vy
    28: "<f",      # vel_2: vz
    29: "<ff",     # coords: lon, lat
    30: "<f",      # altitude
    31: "<ff",     # sigurd temps 1-2
    32: "<ff",     # sigurd temps 3-4
    33: "<ff",     # bat: fjalar, loki volts
}

def apply(pkt_type: int, vals: tuple, t: TelemetryInput) -> None:
    if pkt_type == 20:
        t.flight_state, t.loki_state, t.loki_substate, t.drogue_deployed, t.gnss_fix = vals
    elif pkt_type == 21:
        (t.fafnir_main_valve_pct, t.fafnir_sol_1, t.fafnir_sol_2, t.fafnir_sol_3, t.fafnir_sol_4) = vals
    elif pkt_type == 22:
        (t.thrust,) = vals
    elif pkt_type == 23:
        t.airbrake_safety, t.airbrake_pct = vals
    elif pkt_type == 24:
        t.pyro1, t.pyro2, t.pyro3 = vals
    elif pkt_type == 25:
        t.ax, t.ay = vals
    elif pkt_type == 26:
        (t.az,) = vals
    elif pkt_type == 27:
        t.vx, t.vy = vals
    elif pkt_type == 28:
        (t.vz,) = vals
    elif pkt_type == 29:
        t.longitude, t.latitude = vals
    elif pkt_type == 30:
        (t.altitude,) = vals
    elif pkt_type == 31:
        t.sigurd_temp1, t.sigurd_temp2 = vals
    elif pkt_type == 32:
        t.sigurd_temp3, t.sigurd_temp4 = vals
    elif pkt_type == 33:
        t.fjalar_bat_voltage, t.loki_bat_voltage = vals

def _read_exact(ser: serial.Serial, n: int) -> bytes | None:
    buffer = b""
    while len(buffer) < n:
        chunk = ser.read(n - len(buffer))
        if not chunk:
            return None
        buffer += chunk
    return buffer

def read_packet_blocking(ser: serial.Serial) -> tuple[int, tuple] | None:
    t = _read_exact(ser, 1)
    if not t: return None
    pkt_type = t[2]
    fmt = FMT.get(pkt_type)
    if not fmt: 
        return None
    size = struct.calcsize(fmt)
    payload = _read_exact(ser, size)
    if not payload: 
        return None
    vals = struct.unpack(fmt, payload)
    return pkt_type, vals
