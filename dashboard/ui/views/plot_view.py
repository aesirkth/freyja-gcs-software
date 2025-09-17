import dearpygui.dearpygui as dpg
from ui.utils.value_formatting import format_value
from dashboard.models.input_tel_data import TelemetryInput
from ui.tags_config import PLOT_DASHBOARD

def build(parent: int | str) -> dict:
    with dpg.child_window(parent=parent, tag="plot_dashboard:panel", width=0, height=0, border=False):
        dpg.add_text("Speed: -- m/s", tag=PLOT_DASHBOARD["plot"])
        
    return PLOT_DASHBOARD

def update(data: TelemetryInput, tags: dict) -> None:
    dpg.set_value(tags["plot"], f"Speed: {format_value(data.speed, 'm/s', 1)}")
