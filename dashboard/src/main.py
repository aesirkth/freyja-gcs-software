import dearpygui.dearpygui as dpg

def save_callback():
    print("Save Clicked")

dpg.create_context()

dpg.create_viewport()

dpg.setup_dearpygui()

with dpg.window(label="Example Window"):

    dpg.add_text("Hello world")

    dpg.add_button(label="Save", callback=save_callback)

    dpg.add_input_text(label="string")

    dpg.add_slider_float(label="float")

dpg.show_viewport()

# below replaces, start_dearpygui()
while dpg.is_dearpygui_running():
    # insert here any code you would like to run in the render loop
    # you can manually stop by using stop_dearpygui()
    print("this will run every frame")
    dpg.render_dearpygui_frame()

dpg.destroy_context()
