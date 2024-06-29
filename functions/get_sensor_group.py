import os
import json
import sys

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
# Add the parent directory to the sys.path
sys.path.append(parent_dir)

from classes.sensor_group import sensor_group

def get_sensor_group(group_id):
    # Get the current directory of the script
    current_directory = os.path.dirname(__file__)

    # Specify the path to the sensors JSON file
    sensors_json_file_path = os.path.join(current_directory, "..", "bin", "sensor_groups.json")

    # Open and read the existing sensors JSON file
    with open(sensors_json_file_path, "r") as file:
        sensor_groups = json.load(file)

    for group_info in sensor_groups.values():
        #print("Checking sensor info:", group_info)
        if group_info.get('group_id') == group_id:
            # self, sensor_id, adc_channel, name, sensor_group_id, sensor_cluster_id, unit = None, max_calibration_value = 0, min_calibration_value = 0
            group_object = sensor_group(group_info['group_id'], group_info['sensors'], group_info['name'], group_info['location'], group_info['owner'])
            group_object.sensors = group_info.get('sensors')
            group_object.location = group_info.get('location')
            print(group_object, " found")
            return group_object

    print("Sensor with ID", group_id, "not found")
    return None