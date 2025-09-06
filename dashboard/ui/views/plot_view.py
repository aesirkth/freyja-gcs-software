import dearpygui.dearpygui as dpg
from models.input_data import TelemetryInput
from ui.tags_config import PLOT_DASHBOARD

def build(data: TelemetryInput, parent: int | str) -> dict:
    with dpg.child_window(parent=parent, tag="plot_dashboard:panel", width=0, height=0, border=False):
        dpg.add_text(f"Data: {data["data"] if data.get("data") is not None else "--"} m/s", tag=PLOT_DASHBOARD["plot"])
        
    return PLOT_DASHBOARD
