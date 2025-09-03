import dearpygui.dearpygui as dpg
from ui.tag_config import TAGS

def build(parent: int | str) -> dict:
    with dpg.child_window(parent=parent, tag="dashboard:panel", width=0, height=0, border=False):
        dpg.add_text("Speed: -- °C", tag=TAGS["temp_text"])
        dpg.add_text("Status: --", tag=TAGS["status_text"])
    return TAGS
