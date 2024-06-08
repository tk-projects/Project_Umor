import os
import json
import sys

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
# Add the parent directory to the sys.path
sys.path.append(parent_dir)

from classes.humidity_sensor import humidity_sensor
from functions.get_sensor import get_sensor

def get_sensor_ids():
    sensor_ids_input = input("Enter the sensor IDs separated by commas: ")
    sensor_ids = sensor_ids_input.split(',')
    return [sensor_id.strip() for sensor_id in sensor_ids]

sensor_ids = get_sensor_ids()
number_of_sensors = len(sensor_ids)

if number_of_sensors == 0:
    print("Anzahl an Sensoren nicht korrekt")
    sys.exit()

# Get the current directory of the script
current_directory = os.path.dirname(__file__)

# Specify the path to the sensors JSON file
sensors_json_file_path = os.path.join(current_directory, "..", "bin", "sensors.json")

# Open and read the existing sensors JSON file
with open(sensors_json_file_path, "r") as file:
    sensors_data = json.load(file)

# Create a dictionary to store sensor instances
sensors = {}
for sensor_id in sensor_ids:
    sensor_object = get_sensor(sensor_id)
    print("Sensor isntance of",sensor_object.name, "was succesfully loaded")

    decide_if_calibrate = input(f"Shall sensor {sensor_object.name} be calibrated? (y = calibrate, other keys = no, pass this one): ")

    if decide_if_calibrate == 'y':
        sensor_object.calibrate()

    # Update the sensor data in the JSON structure
    sensors_data[sensor_object.name]['min_calibration_value'] = sensor_object.min_calibration_value
    sensors_data[sensor_object.name]['max_calibration_value'] = sensor_object.max_calibration_value

# Write the updated sensor data back to the JSON file
with open(sensors_json_file_path, "w") as file:
    json.dump(sensors_data, file, indent=4)

print("Sensor data has been updated.")
