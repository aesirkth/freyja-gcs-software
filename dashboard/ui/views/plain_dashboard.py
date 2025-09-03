import dearpygui.dearpygui as dpg
from ui.tag_config import PLAIN_DASHBOARD

def build(parent: int | str) -> dict:
    with dpg.child_window(parent=parent, tag="plain_dashboard:panel", width=0, height=0, border=False):
        dpg.add_text("Speed: -- m/s", tag=PLAIN_DASHBOARD["speed_text"])
        dpg.add_text("Battery Voltage: -- V", tag=PLAIN_DASHBOARD["voltage_text"])
        dpg.add_text("Tank Temperature: -- °C", tag=PLAIN_DASHBOARD["tank_temp_text"])
        dpg.add_text("Injector temperature: -- °C", tag=PLAIN_DASHBOARD["injector_temp_text"])
        dpg.add_text("Post-combustion Chamber Temperature: -- °C", tag=PLAIN_DASHBOARD["post_cc_temp_text"])
        dpg.add_text("Nozzle temperature: -- °C", tag=PLAIN_DASHBOARD["nozzle_temp_text"])
        dpg.add_text("Pressure at injector: -- P", tag=PLAIN_DASHBOARD["injector_pressure_text"])

    return PLAIN_DASHBOARD
