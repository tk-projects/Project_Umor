from  classes.humidity_sensor import humidity_sensor
import os
import json

sensors_file_path = os.path.join(os.getcwd() + "/bin/sensors.json")
print("Loading Sensor Data from: ", sensors_file_path)

with open(sensors_file_path, "r") as json_file:
    sensor_json = json.load(json_file)

print("Loading succesful")

sensors = {}

for sensor_name, sensor_json in sensor_json.items():
    sensors[sensor_name] = humidity_sensor(sensor_json["sensor_id"], sensor_json["adc_channel"], sensor_json["name"], sensor_json["unit"], sensor_json["min_offset"],sensor_json["max_offset"])

print("Sensor data: ", sensors)
    