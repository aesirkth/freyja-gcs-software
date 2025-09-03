import dearpygui.dearpygui as dpg
from ui.tag_config import DASHBOARD

def build(parent: int | str) -> dict:
    with dpg.child_window(parent=parent, tag="dashboard:panel", width=0, height=0, border=False):
        dpg.add_text("Speed: -- m/s", tag=DASHBOARD["speed_text"])
        dpg.add_text("Battery Voltage: -- V", tag=DASHBOARD["voltage_text"])
        dpg.add_text("Tank Temperature: -- °C", tag=DASHBOARD["tank_temp_text"])
        dpg.add_text("Injector temperature: -- °C", tag=DASHBOARD["injector_temp_text"])
        dpg.add_text("Post-combustion Chamber Temperature: -- °C", tag=DASHBOARD["post_cc_temp_text"])
        dpg.add_text("Nozzle temperature: -- °C", tag=DASHBOARD["nozzle_temp_text"])
        dpg.add_text("Pressure at injector: -- P", tag=DASHBOARD["injector_pressure_text"])
    return DASHBOARD
