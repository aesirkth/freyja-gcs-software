import dearpygui.dearpygui as dpg
from ui.views import plot_dashboard
from ui.controllers.data_fetching import fetch_latest_tel_data
from ui.views import propulsion_tab
from ui.views import avionics_tab
from ui.views import recovery_tab
import logging
import asyncio

logger = logging.getLogger(__name__)

async def ui_task():
    try:
        dpg.create_context()
        dpg.create_viewport(title="Example Window", width=1200, height=600, vsync=True)
        dpg.setup_dearpygui()

        dashboard_tags = {"propulsion": {}, "avionics": {}, "recovery": {}, "right": {}}

        with dpg.window(width=1200, height=-1, no_collapse=True, no_resize=True) as primary_window:
            with dpg.group(horizontal=True):
                with dpg.child_window(tag="panel:left", width=280, height=-1, border=True):
                    with dpg.group(horizontal=False):
                        with dpg.child_window(tag="panel:top", width=-1, height=150, border=True):
                            with dpg.tab_bar(tag="tabs:top"):
                                with dpg.tab(label="Propulsion", tag="tab:top:prop"):
                                    dashboard_tags["propulsion"] = propulsion_tab.build(parent="tab:top:prop")

                        with dpg.child_window(tag="panel:middle", width=-1, height=200, border=True):
                            with dpg.tab_bar(tag="tabs:middle"):
                                with dpg.tab(label="Avionics", tag="tab:middle:avio"):
                                    dashboard_tags["avionics"] = avionics_tab.build(parent="tab:middle:avio")

                        with dpg.child_window(tag="panel:bottom", width=-1, height=200, border=True):
                            with dpg.tab_bar(tag="tabs:bottom"):
                                with dpg.tab(label="Recovery", tag="tab:bottom:reco"):
                                    dashboard_tags["recovery"] = recovery_tab.build(parent="tab:bottom:reco")

                with dpg.child_window(tag="panel:right", width=0, height=-1, border=True):
                    with dpg.tab_bar(tag="tabs:right"):
                        with dpg.tab(label="Plot Dashboard", tag="tab:right:plot"):
                            dashboard_tags["right"] = plot_dashboard.build(parent="tab:right:plot")

        dpg.set_primary_window(primary_window, True)
        dpg.show_viewport()

        while dpg.is_dearpygui_running():
            tel = fetch_latest_tel_data()
            propulsion_tab.update(tel, dashboard_tags["propulsion"])
            avionics_tab.update(tel, dashboard_tags["avionics"])
            recovery_tab.update(tel, dashboard_tags["recovery"])
            plot_dashboard.update(tel, dashboard_tags["right"])
            dpg.render_dearpygui_frame()
            await asyncio.sleep(1/60)

        dpg.destroy_context()
    except Exception as e:
        logger.error(f"Error while running DPG ui task. {e}")
