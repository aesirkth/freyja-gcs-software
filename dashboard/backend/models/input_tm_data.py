from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class TelemetryInput(BaseModel):
    start_timestamp_ms: Optional[int] = None
    timestamp_ms: Optional[int] = None
    timestamp: Optional[datetime] = None

    # 0x720
    flight_state: Optional[int] = None
    loki_state: Optional[int] = None
    loki_substate: Optional[int] = None
    drogue_deployed: Optional[bool] = None
    main_deployed: Optional[bool] = None
    gnss_fix: Optional[bool] = None

    # 0x721
    fafnir_main_valve_percentage: Optional[float] = None
    fafnir_motor_solenoid_1: Optional[bool] = None
    fafnir_motor_solenoid_2: Optional[bool] = None
    fafnir_motor_solenoid_3: Optional[bool] = None
    fafnir_motor_solenoid_4: Optional[bool] = None

    # 0x722
    thrust: Optional[float] = None

    # 0x723
    freyr_airbrake_safety_solenoid: Optional[bool] = None
    airbrake_percentage: Optional[float] = None

    # 0x724
    pyro1_fired: Optional[bool] = None
    pyro2_fired: Optional[bool] = None
    pyro3_fired: Optional[bool] = None

    # 0x725
    ax: Optional[float] = None
    ay: Optional[float] = None

    # 0x726
    az: Optional[float] = None

    # 0x727
    vx: Optional[float] = None
    vy: Optional[float] = None

    # 0x72A
    vz: Optional[float] = None

    # 0x72B
    roll: Optional[float] = None
    pitch: Optional[float] = None

    # 0x72C
    yaw: Optional[float] = None

    # 0x72D
    longitude: Optional[float] = None
    latitude: Optional[float] = None

    # 0x72E
    altitude: Optional[float] = None

    # 0x72F
    sigurd_temperature_1: Optional[float] = None
    sigurd_temperature_2: Optional[float] = None

    # 0x730
    sigurd_temperature_3: Optional[float] = None
    sigurd_temperature_4: Optional[float] = None

    # 0x731
    fjalar_bat_voltage: Optional[float] = None
    loki_bat_voltage: Optional[float] = None

    # Location data
    launch_lon: Optional[float] = None
    launch_lat: Optional[float] = None
    east_enu: Optional[float] = None
    north_enu: Optional[float] = None
