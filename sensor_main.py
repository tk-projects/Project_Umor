from  classes.humidity_sensor import humidity_sensor
import os
import json
import time

sensors_file_path = os.path.join(os.getcwd() + "/bin/sensors.json")
print("Loading Sensor Data from: ", sensors_file_path)

with open(sensors_file_path, "r") as json_file:
    sensor_json = json.load(json_file)

print("________________________________________________________________________________________________________")
print("________________________________________________________________________________________________________\n")
print("Initializing")
dauer = 32
for _ in range(dauer):
    print(".", end="", flush=True)
    time.sleep(0.03)

print("")


sensors = {}

for sensor_name, sensor_json in sensor_json.items():
    sensors[sensor_name] = humidity_sensor(sensor_json["sensor_id"], sensor_json["adc_channel"], sensor_json["name"], sensor_json["unit"], sensor_json["max_calibration_value"], sensor_json["min_calibration_value"])
    print("Imported: Sensor",sensor_json["sensor_id"], "| Channel:", sensor_json["adc_channel"], "| max value: ", sensor_json["max_calibration_value"], "| min value:",sensor_json["min_calibration_value"])
    

print("\nSensor data: ", sensors)
    