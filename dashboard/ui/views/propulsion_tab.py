import dearpygui.dearpygui as dpg
from ui.utils.numerical_formatting import format_numerical
from ui.utils.bool_formatting import fmt_bool
from models.input_tm_data import TelemetryInput
from config.tags_config import PLAIN_DASHBOARD

def build(parent: int | str) -> dict:
    with dpg.child_window(parent=parent, tag=PLAIN_DASHBOARD["propulsion:tab"], width=-1, height=-1, border=False):
        with dpg.table(header_row=False, row_background=True, borders_innerH=True, borders_outerH=True, borders_innerV=True, borders_outerV=True):
            dpg.add_table_column(label="Column 1", width_stretch=True, init_width_or_weight=1.0)
            dpg.add_table_column(label="Data col", width_fixed=True, init_width_or_weight=64)

            with dpg.table_row():
                for j in range(0, 2):
                    if j == 0:
                        dpg.add_text("Fafnir main valve:")
                    else:
                        dpg.add_text("--", tag=PLAIN_DASHBOARD["fafnir_main_valve_pct_text"])
            with dpg.table_row():
                for j in range(0, 2):
                    if j == 0:
                        dpg.add_text("Fafnir solenoid 1:")
                    else:
                        dpg.add_text("--", tag=PLAIN_DASHBOARD["fafnir_sol1_text"])
            with dpg.table_row():
                for j in range(0, 2):
                    if j == 0:
                        dpg.add_text("Fafnir solenoid 2:")
                    else:
                        dpg.add_text("--", tag=PLAIN_DASHBOARD["fafnir_sol2_text"])
            with dpg.table_row():
                for j in range(0, 2):
                    if j == 0:
                        dpg.add_text("Fafnir solenoid 3:")
                    else:
                        dpg.add_text("--", tag=PLAIN_DASHBOARD["fafnir_sol3_text"])
            with dpg.table_row():
                for j in range(0, 2):
                    if j == 0:
                        dpg.add_text("Fafnir solenoid 4:")
                    else:
                        dpg.add_text("--", tag=PLAIN_DASHBOARD["fafnir_sol4_text"])

    return PLAIN_DASHBOARD

def update(data: TelemetryInput, tags: dict) -> None:
    dpg.set_value(tags["fafnir_main_valve_pct_text"],
                  f"{format_numerical(getattr(data, "fafnir_main_valve_percentage", None), "%", 2)}")
    dpg.set_value(tags["fafnir_sol1_text"],
                  f"{fmt_bool(getattr(data, "fafnir_motor_solenoid_1", None))}")
    dpg.set_value(tags["fafnir_sol2_text"],
                  f"{fmt_bool(getattr(data, "fafnir_motor_solenoid_2", None))}")
    dpg.set_value(tags["fafnir_sol3_text"],
                  f"{fmt_bool(getattr(data, "fafnirmotor_solenoid_3", None))}")
    dpg.set_value(tags["fafnir_sol4_text"],
                  f"{fmt_bool(getattr(data, "fafnir_motor_solenoid_4", None))}")
