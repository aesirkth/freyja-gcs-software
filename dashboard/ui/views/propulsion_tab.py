import dearpygui.dearpygui as dpg
from ui.utils.value_formatting import format_value
from models.input_tel_data import TelemetryInput
from ui.tags_config import PLAIN_DASHBOARD

def _fmt_bool(val):
    if val is True:  return "Yes"
    if val is False: return "No"
    return "--"

value = [("Flight state", 2), ("Flight state", 5), ("Flight state", 1)]

def build(parent: int | str) -> dict:
    with dpg.child_window(parent=parent, tag=PLAIN_DASHBOARD["propulsion:tab"], width=-1, height=-1, border=False):
        with dpg.table(header_row=False, row_background=True, borders_innerH=True, borders_outerH=True, borders_innerV=True, borders_outerV=True):
            dpg.add_table_column(label="Column 1")
            dpg.add_table_column(label="Data col")

            with dpg.table_row():
                for j in range(0, 2):
                    if j == 0:
                        dpg.add_text("Loki state:")
                    else:
                        dpg.add_text("--", tag=PLAIN_DASHBOARD["loki_state_text"])

    return PLAIN_DASHBOARD

def update(data: TelemetryInput, tags: dict) -> None:
    dpg.set_value(tags["loki_state_text"],
                  f"{format_value(getattr(data, 'loki_state', None), '', 0)}")
   