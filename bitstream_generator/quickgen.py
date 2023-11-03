import dearpygui.dearpygui as dpg
import csv
import os
from bitstream_generator.generate import *

'''
    Hacked together GUI for bitstream generator..
'''
datapath, _ = os.path.split(__file__)
PART_CSV = os.path.join(datapath,"datagen/part_map.csv")

# Store part data in class, dpg like it better this way.
class PartData():
    def __init__(self):
        reader = csv.DictReader(open(PART_CSV))
        self.part_data = [p for p in reader]

# Store some state.
class State():
    def __init__(self):
        self.gen_window = False
        self.target_part = None
    def open_settings(self):
        return self.gen_window

# Init data
part_data = PartData()
state = State()

# Filter parts list callback
def filter_part(sender, value):
    dpg.set_value("part_filter", value)

# Capture target part from rendered part list
def set_target(sender, value, user_data):
    state.target_part = user_data
    state.gen_window = True
    dpg.configure_item("generate", show=True)
    dpg.configure_item("target_part", default_value="Part: " + user_data["PART"])
    dpg.configure_item("target_arch", default_value="Architecture: " + user_data["FULLARCH"])

# Run Bitstream Generator Callback
def generate(sender, value, user_data):
    BS = BitstreamGenerator()
    settings = BitstreamSettings(
            dpg.get_value("perframe"), 
            dpg.get_value("encrypt"),
            dpg.get_value("authenticate")
        ) 
    BS.generate(state.target_part["PART"], settings)
    dpg.configure_item("generate",show=False)
    return


dpg.create_context()
dpg.create_viewport(title="QuickGen", width=770)
dpg.setup_dearpygui()


# Render parts list
with dpg.window(label="Parts", no_close=True):
    dpg.add_input_text(callback=filter_part)
    
    with dpg.filter_set(id="part_filter"): 
        for p in part_data.part_data:
            
            # Dont show versal
            if "versal" in p["ARCH"]:
                continue
            
            with dpg.group(filter_key=p["PART"], horizontal=True):
                for _, v in p.items():
                    dpg.add_text(v)
                dpg.add_button(label="SELECT", callback=set_target, user_data=p)

# Render launch/settings window
with dpg.window(tag="generate", label="Generate", show=False):
    dpg.add_text(tag="target_part")
    dpg.add_text(tag="target_arch")
    with dpg.group(horizontal=True):
        dpg.add_checkbox(tag="perframe", label="PERFRAMECRC")
    with dpg.group(horizontal=True):
        dpg.add_checkbox(tag="encrypt", label="ENCRYPT")
    with dpg.group(horizontal=True):
        dpg.add_checkbox(tag="authenticate", label="AUTHENTICATE")
    dpg.add_button(label="GENERATE", callback=generate)
        
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()
