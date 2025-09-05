import dearpygui.dearpygui as dpg
from ui.tags_config import PLAIN_DASHBOARD
from typing import Dict

def build(data: Dict[str, str | float], parent: int | str) -> dict:
    with dpg.child_window(parent=parent, tag="plain_dashboard:panel", width=0, height=0, border=False):
        dpg.add_text(f"Speed: {data["speed"] if data.get("speed") is not None else "--"} m/s", tag=PLAIN_DASHBOARD["speed_text"])
        dpg.add_text(f"Battery Voltage: {data["battery_voltage"] if data.get("battery_voltage") is not None else "--"} V", tag=PLAIN_DASHBOARD["voltage_text"])
        dpg.add_text(f"Tank Temperature: {data["tank_temp"] if data.get("tank_temp") is not None else "--"} °C", tag=PLAIN_DASHBOARD["tank_temp_text"])
        dpg.add_text(f"Injector temperature: {data["injector_temp"] if data.get("injector_temp") is not None else "--"} °C", tag=PLAIN_DASHBOARD["injector_temp_text"])
        dpg.add_text(f"Post-combustion Chamber Temperature: {data["post_cc_temp"] if data.get("post_cc_temp") is not None else "--"} °C", tag=PLAIN_DASHBOARD["post_cc_temp_text"])
        dpg.add_text(f"Nozzle temperature: {data["nozzle_temp"] if data.get("nozzle_temp") is not None else "--"} °C", tag=PLAIN_DASHBOARD["nozzle_temp_text"])
        dpg.add_text(f"Pressure at injector: {data["injector_pressure"] if data.get("injector_pressure") is not None else "--"} P", tag=PLAIN_DASHBOARD["injector_pressure_text"])

    return PLAIN_DASHBOARD
