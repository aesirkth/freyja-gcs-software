import dearpygui.dearpygui as dpg
from ui.tags_config import PLOT_DASHBOARD

def build(parent: int | str) -> dict:
    with dpg.child_window(parent=parent, tag="plot_dashboard:panel", width=0, height=0, border=False):
        dpg.add_text("Speed: -- m/s", tag=PLOT_DASHBOARD["plot"])
        
    return PLOT_DASHBOARD
