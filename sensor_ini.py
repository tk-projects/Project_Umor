from  classes.humidity_sensor import humidity_sensor
import os
import json

sensor = humidity_sensor(1, 0)
print(sensor)

#sensor.calibrate();


number_of_sensors = 1


# Get the current directory of the script
current_directory = os.path.dirname(__file__)

# Specify the path to the JSON file relative to the current directory
json_file_path = "/bin/sensor_channel_mapping.json"

# Open and read the JSON file
with open(json_file_path, "r") as file:
    sensor_channel_mapping = json.load(file)

print(sensor_channel_mapping)