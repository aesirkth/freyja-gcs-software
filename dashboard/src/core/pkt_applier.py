from .location_calc import calc_enu_location
from models.input_tm_data import TelemetryInput
import struct, logging

logger = logging.getLogger(__name__)

class PacketApplier:
    def __init__(self):
        pass

    def _to_u8(pkt: bytes, byte_index: int):  return pkt[byte_index]
    def _to_b1(pkt: bytes, byte_index: int):  return pkt[byte_index] != 0
    def _to_f32(pkt: bytes, byte_index: int): return struct.unpack_from("<f", pkt, byte_index)[0]

    def _apply_0x700(self, pkt: bytes, tel_object: TelemetryInput):
        tel_object.test_mode    = self._to_b1(pkt, 0)

    def _apply_0x720(self, pkt: bytes, tel_object: TelemetryInput):
        tel_object.flight_state    = self._to_u8(pkt, 0)
        tel_object.loki_state      = self._to_u8(pkt, 1)
        tel_object.loki_substate   = self._to_u8(pkt, 2)
        tel_object.drogue_deployed = self._to_b1(pkt, 3)
        tel_object.main_deployed   = self._to_b1(pkt, 4)
        tel_object.gnss_fix        = self._to_b1(pkt, 5)

    def _apply_0x721(self, pkt: bytes, tel_object: TelemetryInput):
        tel_object.fafnir_main_valve_pct = self._to_f32(pkt, 0)
        tel_object.fafnir_sol_1 = self._to_b1(pkt, 4)
        tel_object.fafnir_sol_2 = self._to_b1(pkt, 5)
        tel_object.fafnir_sol_3 = self._to_b1(pkt, 6)
        tel_object.fafnir_sol_4 = self._to_b1(pkt, 7)

    def _apply_0x722(self, pkt: bytes, tel_object: TelemetryInput): tel_object.thrust = self._to_f32(pkt, 0)
    def _apply_0x723(self, pkt: bytes, tel_object: TelemetryInput): tel_object.airbrake_safety = self._to_b1(pkt, 0); tel_object.airbrake_pct = self._to_f32(pkt, 1)
    def _apply_0x724(self, pkt: bytes, tel_object: TelemetryInput): tel_object.pyro1 = self._to_b1(pkt, 0); tel_object.pyro2 = self._to_b1(pkt, 1); tel_object.pyro3 = self._to_b1(pkt, 2)
    def _apply_0x725(self, pkt: bytes, tel_object: TelemetryInput): tel_object.ax = self._to_f32(pkt, 0); tel_object.ay = self._to_f32(pkt, 4)
    def _apply_0x726(self, pkt: bytes, tel_object: TelemetryInput): tel_object.az = self._to_f32(pkt, 0)
    def _apply_0x727(self, pkt: bytes, tel_object: TelemetryInput): tel_object.vx = self._to_f32(pkt, 0); tel_object.vy = self._to_f32(pkt, 4)
    def _apply_0x72A(self, pkt: bytes, tel_object: TelemetryInput): tel_object.vz = self._to_f32(pkt, 0)
    def _apply_0x72B(self, pkt: bytes, tel_object: TelemetryInput): tel_object.roll = self._to_f32(pkt, 0); tel_object.pitch = self._to_f32(pkt, 4)
    def _apply_0x72C(self, pkt: bytes, tel_object: TelemetryInput): tel_object.yaw = self._to_f32(pkt, 0)

    def _apply_0x72D(self, pkt: bytes, tel_object: TelemetryInput):
        tel_object.longitude = self._to_f32(pkt, 0)
        tel_object.latitude  = self._to_f32(pkt, 4)

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

    def _apply_0x72E(self, pkt: bytes, tel_object: TelemetryInput): tel_object.altitude = self._to_f32(pkt, 0)
    def _apply_0x72F(self, pkt: bytes, tel_object: TelemetryInput): tel_object.sigurd_temp1 = self._to_f32(pkt, 0); tel_object.sigurd_temp2 = self._to_f32(pkt, 4)
    def _apply_0x730(self, pkt: bytes, tel_object: TelemetryInput): tel_object.sigurd_temp3 = self._to_f32(pkt, 0); tel_object.sigurd_temp4 = self._to_f32(pkt, 4)
    def _apply_0x731(self, pkt: bytes, tel_object: TelemetryInput): tel_object.fjalar_bat_voltage = self._to_f32(pkt, 0); tel_object.loki_bat_voltage = self._to_f32(pkt, 4)

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
