import dearpygui.dearpygui as dpg
from models.input_tel_data import TelemetryInput
from ui.tags_config import PLOT_DASHBOARD

def build(parent: int | str) -> dict:
    with dpg.child_window(parent=parent, tag=PLOT_DASHBOARD["location:panel"], width=0, height=0, border=False):
        with dpg.plot(height=400, width=-1) as plot_id:
            dpg.add_plot_legend()
            x_axis = dpg.add_plot_axis(dpg.mvXAxis, label="x")
            y_axis = dpg.add_plot_axis(dpg.mvYAxis, label="y")
            line_id = dpg.add_scatter_series([0], [0], label="Position", parent=y_axis, tag=PLOT_DASHBOARD["enu_location"])
            dpg.fit_axis_data(x_axis)
            dpg.fit_axis_data(y_axis)

        PLOT_DASHBOARD["plot_id"] = plot_id
        PLOT_DASHBOARD["x_axis"] = x_axis
        PLOT_DASHBOARD["y_axis"] = y_axis
        PLOT_DASHBOARD["line_id"] = line_id

    return PLOT_DASHBOARD

def update(data: TelemetryInput, tags: dict) -> None:
    dpg.set_value(tags["enu_location"], [[data.east_enu], [data.north_enu]])
