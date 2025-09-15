import asyncio, serial
from .core.can_conversion import apply, read_packet_blocking
from models.input_data import TelemetryInput
from src.state.bus import telemetry_queue
import logging

logger = logging.getLogger(__name__)

async def core_serial_task(port="/dev/ttyUSB0", baud=115200):
    try:    
        ser = serial.Serial(port, baudrate=baud, timeout=0.2)
        latest_tel_data = TelemetryInput()
        while True:
            pkt = await asyncio.to_thread(read_packet_blocking, ser)
            if not pkt:
                await asyncio.sleep(0)  # yield
                continue
            can_pkt_type, can_pkt_data = pkt
            apply(can_pkt_type, can_pkt_data, latest_tel_data)

            if telemetry_queue.full():
                _ = telemetry_queue.get_nowait()
            await telemetry_queue.put(latest_tel_data)
            await asyncio.sleep(0.01) 
            """
            tel_data = TelemetryInput(
                speed=random.random()*50,
                battery_voltage=random.random()*50,
                tank_temp=random.random()*50,
            )
            await telemetry_queue.put(tel_data)
            """
    except Exception as e:
        logger.error(f"Error while running core serial task. {e}")
    finally:
        ser.close()
