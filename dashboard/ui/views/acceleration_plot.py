from math import sin
import dearpygui.dearpygui as dpg
from models.input_tel_data import TelemetryInput
from ui.tags_config import PLOT_DASHBOARD

xs = [i / 1000 for i in range(500)]
ys = [0.5 + 0.5 * sin(50 * x) for x in xs]

def build(parent: int | str) -> dict:
    with dpg.child_window(parent=parent, tag=PLOT_DASHBOARD["acceleration:panel"], width=0, height=0, border=False):
        with dpg.plot(height=400, width=-1) as plot_id:
            dpg.add_plot_legend()
            x_axis = dpg.add_plot_axis(dpg.mvXAxis, label="x")
            y_axis = dpg.add_plot_axis(dpg.mvYAxis, label="y")
            line_id = dpg.add_scatter_series(xs, ys, parent=y_axis, tag=PLOT_DASHBOARD["acceleration"])
            dpg.fit_axis_data(x_axis)
            dpg.fit_axis_data(y_axis)

    return PLOT_DASHBOARD

def update(data: TelemetryInput, tags: dict) -> None:
    dpg.set_value(tags["acceleration"], [[data.east_enu], [data.north_enu]])
