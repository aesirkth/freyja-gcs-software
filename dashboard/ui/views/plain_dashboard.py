import dearpygui.dearpygui as dpg

TAGS = {
    "temp_text": "dashboard:temp_text",
    "status_text": "dashboard:status_text",
}

def build(parent: int | str) -> dict:
    with dpg.child_window(parent=parent, tag="dashboard:panel", width=0, height=0, border=False):
        dpg.add_text("Temp: -- °C", tag=TAGS["temp_text"])
        dpg.add_text("Status: --", tag=TAGS["status_text"])
    return TAGS
