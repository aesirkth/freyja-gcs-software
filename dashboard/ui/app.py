import dearpygui.dearpygui as dpg
from ui.controllers.data_fetching import fetch_latest_tel_data
from ui.views import propulsion_tab
from ui.views import avionics_tab
from ui.views import recovery_tab
from ui.views import location_plot
from ui.views import velocity_plot
from ui.views import acceleration_plot
import logging
import asyncio

logger = logging.getLogger(__name__)

async def ui_task():
    try:
        dpg.create_context()
        dpg.create_viewport(title="Example Window", width=1200, height=600, vsync=True)
        dpg.setup_dearpygui()

        dashboard_tags = {
            "propulsion": {},
            "avionics": {},
            "recovery": {},
            "location": {},
            "velocity": {},
            "acceleration": {},
        }

        with dpg.window(width=1200, height=-1, no_collapse=True, no_resize=True) as primary_window:
            with dpg.group(horizontal=True):
                with dpg.child_window(tag="panel:left", width=280, height=-1, border=True):
                    with dpg.group(horizontal=False):
                        with dpg.child_window(tag="panel:left:top", width=-1, height=160, border=False):
                            with dpg.tab_bar(tag="tabs:left:top"):
                                with dpg.tab(label="Propulsion", tag="tab:left:top:prop"):
                                    dashboard_tags["propulsion"] = propulsion_tab.build(parent="tab:left:top:prop")

                        with dpg.child_window(tag="panel:left:middle", width=-1, height=200, border=False):
                            with dpg.tab_bar(tag="tabs:left:middle"):
                                with dpg.tab(label="Avionics", tag="tab:left:middle:avio"):
                                    dashboard_tags["avionics"] = avionics_tab.build(parent="tab:left:middle:avio")

                        with dpg.child_window(tag="panel:left:bottom", width=-1, height=160, border=False):
                            with dpg.tab_bar(tag="tabs:left:bottom"):
                                with dpg.tab(label="Recovery", tag="tab:left:bottom:reco"):
                                    dashboard_tags["recovery"] = recovery_tab.build(parent="tab:left:bottom:reco")

                with dpg.child_window(tag="panel:right:first", width=350, height=-1, border=False):
                    with dpg.child_window(tag="panel:right:first:top", width=-1, border=False):
                        with dpg.tab_bar(tag="tabs:right:first:top"):
                            with dpg.tab(label="Location (ENU)", tag="tab:right:first:top:plot"):
                                dashboard_tags["location"] = location_plot.build(parent="tab:right:first:top:plot")

                with dpg.child_window(tag="panel:right:second", width=350, height=-1, border=False):
                    with dpg.child_window(tag="panel:right:second:top", width=-1, border=False):
                        with dpg.tab_bar(tag="tabs:right:second:top"):
                            with dpg.tab(label="Velocity", tag="tab:right:second:top:plot"):
                                dashboard_tags["velocity"] = velocity_plot.build(parent="tab:right:second:top:plot")

                with dpg.child_window(tag="panel:right:third", width=350, height=-1, border=False):
                    with dpg.child_window(tag="panel:right:third:top", width=-1, border=False):
                        with dpg.tab_bar(tag="tabs:right:third:top"):
                            with dpg.tab(label="Acceleration", tag="tab:right:third:top:plot"):
                                dashboard_tags["acceleration"] = acceleration_plot.build(parent="tab:right:third:top:plot")

        dpg.set_primary_window(primary_window, True)
        dpg.show_viewport()

        while dpg.is_dearpygui_running():
            tel = await fetch_latest_tel_data()
            propulsion_tab.update(tel, dashboard_tags["propulsion"])
            avionics_tab.update(tel, dashboard_tags["avionics"])
            recovery_tab.update(tel, dashboard_tags["recovery"])
            location_plot.update(tel, dashboard_tags["location"])
            velocity_plot.update(tel, dashboard_tags["velocity"])
            velocity_plot.update(tel, dashboard_tags["acceleration"])
            dpg.render_dearpygui_frame()
            await asyncio.sleep(0)

        dpg.destroy_context()
    except Exception as e:
        logger.exception(f"Error while running DPG ui task. {e}")
