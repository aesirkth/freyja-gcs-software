from pydantic import BaseModel
from typing import Optional

class TelemetryInput(BaseModel):
    speed: Optional[float] = None
    battery_voltage: Optional[float] = None
    tank_temp: Optional[float] = None
    injector_temp: Optional[float] = None
    post_cc_temp: Optional[float] = None
    nozzle_temp: Optional[float] = None
    injector_pressure: Optional[float] = None
    