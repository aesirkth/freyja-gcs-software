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
    with dpg.child_window(parent=parent, tag=PLAIN_DASHBOARD["avionics:tab"], width=-1, height=-1, border=False):
        with dpg.collapsing_header(label="States", default_open=True):
            # dpg.add_text("Flight state: --", tag=PLAIN_DASHBOARD["flight_state_text"])
            # dpg.add_text("Loki state: --", tag=PLAIN_DASHBOARD["loki_state_text"])
            dpg.add_text("Loki substate: --", tag=PLAIN_DASHBOARD["loki_substate_text"])

        with dpg.collapsing_header(label="Recovery & GNSS", default_open=True):
            dpg.add_text("Drogue deployed: --", tag=PLAIN_DASHBOARD["drogue_deployed_text"])
            dpg.add_text("Main deployed: --", tag=PLAIN_DASHBOARD["main_deployed_text"])
            dpg.add_text("GNSS fix: --", tag=PLAIN_DASHBOARD["gnss_fix_text"])

        with dpg.collapsing_header(label="Fafnir (Actuators)", default_open=True):
            dpg.add_text("Motor solenoid 1: --", tag=PLAIN_DASHBOARD["fafnir_sol1_text"])
            dpg.add_text("Motor solenoid 2: --", tag=PLAIN_DASHBOARD["fafnir_sol2_text"])
            dpg.add_text("Motor solenoid 3: --", tag=PLAIN_DASHBOARD["fafnir_sol3_text"])
            dpg.add_text("Motor solenoid 4: --", tag=PLAIN_DASHBOARD["fafnir_sol4_text"])

        with dpg.collapsing_header(label="Freyr / Airbrake", default_open=True):
            dpg.add_text("Safety solenoid: --", tag=PLAIN_DASHBOARD["freyr_airbrake_safety_text"])

        with dpg.collapsing_header(label="Pyrotechnics", default_open=True):
            dpg.add_text("Pyro 1 fired: --", tag=PLAIN_DASHBOARD["pyro1_text"])
            dpg.add_text("Pyro 2 fired: --", tag=PLAIN_DASHBOARD["pyro2_text"])
            dpg.add_text("Pyro 3 fired: --", tag=PLAIN_DASHBOARD["pyro3_text"])

    return PLAIN_DASHBOARD

def update(data: TelemetryInput, tags: dict) -> None:
    dpg.set_value(tags["loki_substate_text"],
                  f"Loki substate: {format_value(getattr(data, 'loki_substate', None), '', 0)}")

    dpg.set_value(tags["drogue_deployed_text"],
                  f"Drogue deployed: {_fmt_bool(getattr(data, 'drogue_deployed', None))}")
    dpg.set_value(tags["main_deployed_text"],
                  f"Main deployed: {_fmt_bool(getattr(data, 'main_deployed', None))}")
    dpg.set_value(tags["gnss_fix_text"],
                  f"GNSS fix: {_fmt_bool(getattr(data, 'gnss_fix', None))}")

    dpg.set_value(tags["fafnir_sol1_text"],
                  f"Motor solenoid 1: {_fmt_bool(getattr(data, 'fafnir_motor_solenoid_1', None))}")
    dpg.set_value(tags["fafnir_sol2_text"],
                  f"Motor solenoid 2: {_fmt_bool(getattr(data, 'fafnir_motor_solenoid_2', None))}")
    dpg.set_value(tags["fafnir_sol3_text"],
                  f"Motor solenoid 3: {_fmt_bool(getattr(data, 'fafnir_motor_solenoid_3', None))}")
    dpg.set_value(tags["fafnir_sol4_text"],
                  f"Motor solenoid 4: {_fmt_bool(getattr(data, 'fafnir_motor_solenoid_4', None))}")

    dpg.set_value(tags["freyr_airbrake_safety_text"],
                  f"Safety solenoid: {_fmt_bool(getattr(data, 'freyr_airbrake_safety_solenoid', None))}")

    dpg.set_value(tags["pyro1_text"], f"Pyro 1 fired: {_fmt_bool(getattr(data, 'pyro1_fired', None))}")
    dpg.set_value(tags["pyro2_text"], f"Pyro 2 fired: {_fmt_bool(getattr(data, 'pyro2_fired', None))}")
    dpg.set_value(tags["pyro3_text"], f"Pyro 3 fired: {_fmt_bool(getattr(data, 'pyro3_fired', None))}")
