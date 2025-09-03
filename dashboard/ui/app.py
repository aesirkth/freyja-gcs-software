import time
import dearpygui.dearpygui as dpg
from ui.views import plain_dashboard, plot_view

def save_callback():
    print("Save Clicked")

dpg.create_context()
dpg.create_viewport(title="Example Window", width=1200, height=600, vsync=True)
dpg.setup_dearpygui()

with dpg.window(width=1200, height=600, no_collapse=True, no_resize=True):
    dpg.add_text("Hello world")
    dpg.add_button(label="Save", callback=save_callback)
    dpg.add_input_text(label="string")
    dpg.add_slider_float(label="float")

    with dpg.group(horizontal=True):
        with dpg.child_window(tag="panel:left", width=520, height=-1, border=True):
            with dpg.tab_bar(tag="tabs:left"):
                with dpg.tab(label="Plain Dashboard", tag="tab:left:dash"):
                    plain_dashboard.build(parent="tab:left:dash")

        with dpg.child_window(tag="panel:right", width=0, height=-1, border=True):
            with dpg.tab_bar(tag="tabs:right"):
                with dpg.tab(label="Plot Dashboard", tag="tab:right:plot"):
                    plot_view.build(parent="tab:right:plot")

dpg.show_viewport()

while dpg.is_dearpygui_running():
    dpg.render_dearpygui_frame()
    time.sleep(1/60)

dpg.destroy_context()
