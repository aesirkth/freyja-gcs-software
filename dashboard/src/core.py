import asyncio, random
from dashboard.models.input_data import TelemetryInput
from state.bus import telemetry_q

async def core_loop():
    while True:
        tel = TelemetryInput(
            speed=20 + random.random()*5,
            battery_voltage=12.1,
            tank_temp=35.0,
        )
        if telemetry_q.full():
            _ = telemetry_q.get_nowait()
        await telemetry_q.put(tel)
        await asyncio.sleep(0.01) 
        