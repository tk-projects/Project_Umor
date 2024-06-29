import os
import json
import sys

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
# Add the parent directory to the sys.path
sys.path.append(parent_dir)

def load_sensor_json():
    # Get the current directory of the script
    current_directory = os.path.dirname(__file__)

    # Specify the path to the sensors JSON file
    sensors_json_file_path = os.path.join(current_directory, "..", "bin", "sensors.json")

    # Open and read the existing sensors JSON file
    with open(sensors_json_file_path, "r") as file:
        sensors_data = json.load(file)
    
    return sensors_data