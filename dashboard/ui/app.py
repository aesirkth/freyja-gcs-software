import dearpygui.dearpygui as dpg
from ui.views import plain_dashboard

def save_callback():
    print("Save Clicked")

dpg.create_context()

dpg.create_viewport()

dpg.setup_dearpygui()

with dpg.window(width=1200, height=600, label="Example Window") as window:
    dpg.add_text("Hello world")

    dpg.add_button(label="Save", callback=save_callback)

    dpg.add_input_text(label="string")

    dpg.add_slider_float(label="float")

    with dpg.tab_bar(tag="tabs"):
        with dpg.tab(label="Dashboard", tag="tab:dash"):
            dash_tags = plain_dashboard.build(parent="tab:dash")

dpg.show_viewport()

# below replaces, start_dearpygui()
while dpg.is_dearpygui_running():
    # Manually stop by using stop_dearpygui()
    print("this will run every frame")
    dpg.render_dearpygui_frame()

dpg.destroy_context()
