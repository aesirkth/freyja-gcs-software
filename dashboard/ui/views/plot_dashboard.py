from math import sin
import dearpygui.dearpygui as dpg
from dashboard.ui.utils.numerical_formatting import format_value
from models.input_tel_data import TelemetryInput
from ui.tags_config import PLOT_DASHBOARD

xs = [i / 1000 for i in range(500)]
ys = [0.5 + 0.5 * sin(50 * x) for x in xs]

def build(parent: int | str) -> dict:
    with dpg.child_window(parent=parent, tag="plot_dashboard:panel", width=0, height=0, border=False):
        dpg.add_text("Speed: -- m/s", tag=PLOT_DASHBOARD["plot"])
    
        with dpg.plot(label="Line Series", height=400, width=-1) as plot_id:
            dpg.add_plot_legend()
            x_axis = dpg.add_plot_axis(dpg.mvXAxis, label="x")
            y_axis = dpg.add_plot_axis(dpg.mvYAxis, label="y")
            line_id = dpg.add_line_series(xs, ys, label="demo sin", parent=y_axis, tag=PLOT_DASHBOARD["enu_location"])
            dpg.fit_axis_data(x_axis)
            dpg.fit_axis_data(y_axis)

        PLOT_DASHBOARD["plot_id"] = plot_id
        PLOT_DASHBOARD["x_axis"] = x_axis
        PLOT_DASHBOARD["y_axis"] = y_axis
        PLOT_DASHBOARD["line_id"] = line_id
        
    return PLOT_DASHBOARD

def update(data: TelemetryInput, tags: dict) -> None:
    data = TelemetryInput()
    # dpg.set_value(tags["plot"], f"Speed: {format_value(data.altitude, 'm/s', 1)}")
    dpg.set_value(tags["enu_location"], [xs, ys])
