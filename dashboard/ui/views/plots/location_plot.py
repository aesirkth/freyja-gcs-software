import dearpygui.dearpygui as dpg
from models.input_tel_data import TelemetryInput
from ui.tags_config import PLOT_DASHBOARD

def build(parent: int | str) -> dict:
    with dpg.child_window(parent=parent, tag=PLOT_DASHBOARD["location:panel"], width=0, height=0, border=False):
        with dpg.plot(height=400, width=-1) as plot_id:
            x_axis = dpg.add_plot_axis(dpg.mvXAxis, label="E/W")
            y_axis = dpg.add_plot_axis(dpg.mvYAxis, label="N/S")
            current_location_id = dpg.add_scatter_series([0], [0], label=" Current Position", parent=y_axis, tag=PLOT_DASHBOARD["enu_location"])
            init_location_id = dpg.add_scatter_series([0], [0], label=" Launch Position", parent=y_axis, tag=PLOT_DASHBOARD["launch_location"])
            dpg.fit_axis_data(x_axis)
            dpg.fit_axis_data(y_axis)

        PLOT_DASHBOARD["plot_id"] = plot_id
        PLOT_DASHBOARD["x_axis"] = x_axis
        PLOT_DASHBOARD["y_axis"] = y_axis
        PLOT_DASHBOARD["current_location_id"] = current_location_id
        PLOT_DASHBOARD["init_location_id_id"] = init_location_id

    return PLOT_DASHBOARD

def update(data: TelemetryInput, tags: dict) -> None:
    dpg.set_value(tags["launch_location"], [[18], [59]])
    dpg.set_value(tags["enu_location"], [[data.east_enu], [data.north_enu]])
