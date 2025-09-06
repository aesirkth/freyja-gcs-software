import dearpygui.dearpygui as dpg
from models.input_data import TelemetryInput
from ui.tags_config import PLOT_DASHBOARD

def _format(val, unit, digits=1):
    if val is None:
        return f"-- {unit}"
    if isinstance(val, float):
        return f"{val:.{digits}f} {unit}"
    return f"{val} {unit}"

def build(parent: int | str) -> dict:
    with dpg.child_window(parent=parent, tag="plot_dashboard:panel", width=0, height=0, border=False):
        dpg.add_text("Speed: -- m/s", tag=PLOT_DASHBOARD["plot"])
        
    return PLOT_DASHBOARD

def update(data: TelemetryInput, tags: dict) -> None:
    dpg.set_value(tags["plot"], f"Speed: {_format(data.speed, 'm/s', 1)}")
    
   