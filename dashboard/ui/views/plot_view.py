import dearpygui.dearpygui as dpg
from ui.tags_config import PLOT_DASHBOARD
from typing import Dict

def build(data: Dict[str, str | float], parent: int | str) -> dict:
    with dpg.child_window(parent=parent, tag="plot_dashboard:panel", width=0, height=0, border=False):
        dpg.add_text(f"Data: {data["data"] if data.get("data") is not None else "--"} m/s", tag=PLOT_DASHBOARD["plot"])
        
    return PLOT_DASHBOARD
