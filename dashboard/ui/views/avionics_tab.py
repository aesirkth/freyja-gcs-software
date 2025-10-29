import dearpygui.dearpygui as dpg
from ui.utils.numerical_formatting import format_numerical
from ui.utils.bool_formatting import fmt_bool
from models.input_tel_data import TelemetryInput
from ui.tags_config import PLAIN_DASHBOARD

def build(parent: int | str) -> dict:
    with dpg.child_window(parent=parent, tag=PLAIN_DASHBOARD["avionics:tab"], width=-1, height=-1, border=False):
        with dpg.table(header_row=False, row_background=True, borders_innerH=True, borders_outerH=True, borders_innerV=True, borders_outerV=True):
            dpg.add_table_column(label="Column 1", width_stretch=True, init_width_or_weight=1.0)
            dpg.add_table_column(label="Data col", width_fixed=True, init_width_or_weight=64)

            with dpg.table_row():
                for j in range(0, 2):
                    if j == 0:
                        dpg.add_text("Flight state:")
                    else:
                        dpg.add_text("--", tag=PLAIN_DASHBOARD["flight_state_text"])
            with dpg.table_row():
                for j in range(0, 2):
                    if j == 0:
                        dpg.add_text("Loki state:")
                    else:
                        dpg.add_text("--", tag=PLAIN_DASHBOARD["loki_state_text"])
            with dpg.table_row():
                for j in range(0, 2):
                    if j == 0:
                        dpg.add_text("Loki substate:")
                    else:
                        dpg.add_text("--", tag=PLAIN_DASHBOARD["loki_substate_text"])
            with dpg.table_row():
                for j in range(0, 2):
                    if j == 0:
                        dpg.add_text("GNSS fix:")
                    else:
                        dpg.add_text("--", tag=PLAIN_DASHBOARD["gnss_fix_text"])
            with dpg.table_row():
                for j in range(0, 2):
                    if j == 0:
                        dpg.add_text("Fjalar battery:")
                    else:
                        dpg.add_text("--", tag=PLAIN_DASHBOARD["fjalar_bat_voltage_text"])
            with dpg.table_row():
                for j in range(0, 2):
                    if j == 0:
                        dpg.add_text("Loki battery:")
                    else:
                        dpg.add_text("--", tag=PLAIN_DASHBOARD["loki_bat_voltage_text"])

    return PLAIN_DASHBOARD

def update(data: TelemetryInput, tags: dict) -> None:
    dpg.set_value(tags["flight_state_text"],
                  f"{getattr(data, "flight_state", None)}")
    dpg.set_value(tags["loki_state_text"],
                  f"{getattr(data, "loki_state", None)}")
    dpg.set_value(tags["loki_substate_text"],
                  f"{getattr(data, "loki_substate", None)}")
    dpg.set_value(tags["gnss_fix_text"],
                  f"{getattr(data, "gnss_fix", None)}")
    dpg.set_value(tags["fjalar_bat_voltage_text"],
                  f"{format_numerical(getattr(data, "fjalar_bat_voltage", None), "V")}")
    dpg.set_value(tags["loki_bat_voltage_text"],
                  f"{format_numerical(getattr(data, "loki_bat_voltage", None), "V")}")
    