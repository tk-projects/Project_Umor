import os
import json
import sys

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
# Add the parent directory to the sys.path
sys.path.append(parent_dir)

from classes.humidity_sensor import humidity_sensor

def get_sensor(sensor_id):
    # Get the current directory of the script
    current_directory = os.path.dirname(__file__)

    # Specify the path to the sensors JSON file
    sensors_json_file_path = os.path.join(current_directory, "..", "bin", "sensors.json")

    # Open and read the existing sensors JSON file
    with open(sensors_json_file_path, "r") as file:
        sensors_data = json.load(file)

    for sensor_info in sensors_data.values():
        #print("Checking sensor info:", sensor_info)
        if sensor_info.get('sensor_id') == sensor_id:
            # self, sensor_id, adc_channel, name, sensor_group_id, sensor_cluster_id, unit = None, max_calibration_value = 0, min_calibration_value = 0
            sensor_object = humidity_sensor(sensor_info['sensor_id'], sensor_info['adc_channel'], sensor_info['name'], sensor_info['sensor_group'], sensor_info['sensor_cluster'], sensor_info['unit'])
            sensor_object.min_calibration_value = sensor_info.get('min_calibration_value', 0)
            sensor_object.max_calibration_value = sensor_info.get('max_calibration_value', 0)
            sensor_object.sensor_group_id = sensor_info.get('sensor_group', 0)
            print(sensor_object, " found")
            return sensor_object

    print("Sensor with ID", sensor_id, "not found")
    return None
