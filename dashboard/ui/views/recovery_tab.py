import dearpygui.dearpygui as dpg
from dashboard.ui.utils.numerical_formatting import format_value
from models.input_tel_data import TelemetryInput
from ui.tags_config import PLAIN_DASHBOARD

def _fmt_bool(val):
    if val is True:  return "Yes"
    if val is False: return "No"
    return "--"

value = [("Flight state", 2), ("Flight state", 5), ("Flight state", 1)]

def build(parent: int | str) -> dict:
    with dpg.child_window(parent=parent, tag=PLAIN_DASHBOARD["recovery:tab"], width=-1, height=-1, border=False):
        with dpg.table(header_row=False, row_background=True, borders_innerH=True, borders_outerH=True, borders_innerV=True, borders_outerV=True):
            dpg.add_table_column(label="Column 1", width_stretch=True, init_width_or_weight=1.0)
            dpg.add_table_column(label="Data col", width_fixed=True, init_width_or_weight=64)

            with dpg.table_row():
                for j in range(0, 2):
                    if j == 0:
                        dpg.add_text("Pyro1 fired/connect:")
                    else:
                        dpg.add_text("--", tag=PLAIN_DASHBOARD["pyro1_text"])
            with dpg.table_row():
                for j in range(0, 2):
                    if j == 0:
                        dpg.add_text("Pyro2 fired/conect:")
                    else:
                        dpg.add_text("--", tag=PLAIN_DASHBOARD["pyro2_text"])
            with dpg.table_row():
                for j in range(0, 2):
                    if j == 0:
                        dpg.add_text("Pyro3 fired/connect:")
                    else:
                        dpg.add_text("--", tag=PLAIN_DASHBOARD["pyro3_text"])
            with dpg.table_row():
                for j in range(0, 2):
                    if j == 0:
                        dpg.add_text("Drogue deployed:")
                    else:
                        dpg.add_text("--", tag=PLAIN_DASHBOARD["drogue_deployed_text"])
            with dpg.table_row():
                for j in range(0, 2):
                    if j == 0:
                        dpg.add_text("Main deployed:")
                    else:
                        dpg.add_text("--", tag=PLAIN_DASHBOARD["main_deployed_text"])

    return PLAIN_DASHBOARD

def update(data: TelemetryInput, tags: dict) -> None:
    dpg.set_value(tags["pyro1_text"],
                  f"{_fmt_bool(getattr(data, "pyro1_fired", None))}")
    dpg.set_value(tags["pyro2_text"],
                  f"{_fmt_bool(getattr(data, "pyro2_fired", None))}")
    dpg.set_value(tags["pyro3_text"],
                  f"{_fmt_bool(getattr(data, "pyro3_fired", None))}")
    
    dpg.set_value(tags["drogue_deployed_text"],
                  f"{_fmt_bool(getattr(data, "drogue_deployed", None))}")
    dpg.set_value(tags["main_deployed_text"],
                  f"{_fmt_bool(getattr(data, "main_deployed", None))}")
   