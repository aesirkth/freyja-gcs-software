import dearpygui.dearpygui as dpg
from ui.controllers.data_fetching import fetch_latest_tel_data
from ui.views import plain_dashboard, plot_view
import logging
import asyncio

logger = logging.getLogger(__name__)

async def ui_task():
    try:
        dpg.create_context()
        dpg.create_viewport(title="Example Window", width=1200, height=600, vsync=True)
        dpg.setup_dearpygui()

        dashboard_tags = {"left": {}, "right": {}}

        with dpg.window(width=1200, height=600, no_collapse=True, no_resize=True) as primary_window:
            with dpg.group(horizontal=True):
                with dpg.child_window(tag="panel:left", width=520, height=-1, border=True):
                    with dpg.tab_bar(tag="tabs:left"):
                        with dpg.tab(label="Plain Dashboard", tag="tab:left:dash"):
                            dashboard_tags["left"] = plain_dashboard.build(parent="tab:left:dash")

                with dpg.child_window(tag="panel:right", width=0, height=-1, border=True):
                    with dpg.tab_bar(tag="tabs:right"):
                        with dpg.tab(label="Plot Dashboard", tag="tab:right:plot"):
                            dashboard_tags["right"] = plot_view.build(parent="tab:right:plot")

        dpg.set_primary_window(primary_window, True)
        dpg.show_viewport()

        while dpg.is_dearpygui_running():
            tel = await fetch_latest_tel_data()
            plain_dashboard.update(tel, dashboard_tags["left"])
            dpg.render_dearpygui_frame()
            await asyncio.sleep(1/60)

        dpg.destroy_context()
    except Exception as e:
        logger.error(f"Error while running DPG ui task. {e}")
