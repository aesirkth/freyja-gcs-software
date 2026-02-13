import dearpygui.dearpygui as dpg
from src.state.cmd_queue import cmd_queue
from models.gcs_state import GCSState
from dashboard.config.tags_config import TEST_MODE_DASHBOARD, COMMAND_CONFIG

def queue_command(cmd_id, app_data):
    cmd_queue.put(COMMAND_CONFIG[cmd_id])
    print(f"Command {cmd_id} queued")
    dpg.set_value("text item", f"Mouse Button ID: {app_data}")

def build(parent: int | str) -> dict:
    with dpg.child_window(parent=parent, tag=TEST_MODE_DASHBOARD["avionics:tab"], width=-1, height=-1, border=False):
        with dpg.table(header_row=False, row_background=True, borders_innerH=True, borders_outerH=True, borders_innerV=True, borders_outerV=True):
            dpg.add_table_column(label="Column 1", width_stretch=True, init_width_or_weight=1.0)
            dpg.add_table_column(label="Data col", width_fixed=True, init_width_or_weight=64)

            with dpg.table_row(label="h", callback=queue_command):
                for j in range(0, 2):
                    if j == 0:
                        dpg.add_text("Flight state:")
                    else:
                        dpg.add_text("--", tag=TEST_MODE_DASHBOARD["flight_state_text"])

    return TEST_MODE_DASHBOARD

def update(data: GCSState, tags: dict) -> None:
    dpg.set_value(tags["flight_state_text"],
                  f"{getattr(data, "flight_state", None)}")
    