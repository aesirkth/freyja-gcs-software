import dearpygui.dearpygui as dpg
from ui.utils.value_formatting import format_value
from dashboard.models.input_tel_data import TelemetryInput
from ui.tags_config import PLAIN_DASHBOARD

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

def update(data: TelemetryInput, tags: dict) -> None:
    dpg.set_value(tags["speed_text"], f"Speed: {format_value(data.speed, 'm/s', 1)}")
    dpg.set_value(tags["voltage_text"], f"Battery Voltage: {format_value(data.battery_voltage, 'V', 2)}")
    dpg.set_value(tags["tank_temp_text"], f"Tank Temperature: {format_value(data.tank_temp, '°C', 1)}")
    dpg.set_value(tags["injector_temp_text"], f"Injector temperature: {format_value(data.injector_temp, '°C', 1)}")
    dpg.set_value(tags["post_cc_temp_text"], f"Post-combustion Chamber Temperature: {format_value(data.post_cc_temp, '°C', 1)}")
    dpg.set_value(tags["nozzle_temp_text"], f"Nozzle temperature: {format_value(data.nozzle_temp, '°C', 1)}")
    dpg.set_value(tags["injector_pressure_text"], f"Pressure at injector: {format_value(data.injector_pressure, 'P', 1)}")
  