from  classes.humidity_sensor import humidity_sensor
import os
import json
import sys


#sensor = humidity_sensor(1, 0)
#print(sensor)


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

# Specify the path to the JSON file relative to the current directory
json_file_path = os.path.join(current_directory , "..", "/bin/sensor_channel_mapping.json")

# Open and read the JSON file
with open(json_file_path, "r") as file:
    sensor_channel_mapping = json.load(file)

# Create a dictionary to store sensor instances
sensors = {}
for i, sensor_id in enumerate(sensor_ids, start=1):
    sensor_name = f"sensor_{sensor_id}"
    sensor_channel = sensor_channel_mapping.get(sensor_name, "Error: Sensor nicht gefunden. Prüfe die sensor_channel_mapping.json Datei im Ordner /bin/ !")
    sensor_object = humidity_sensor(i, sensor_channel, sensor_name, "%")

    decide_if_calibrate = input(f"Shall sensor {sensor_name} be calibrated? (y = calibrate, other keys = no, pass this one): ")

    if decide_if_calibrate == 'y':
        sensor_object.calibrate()
    else:
        sensor_object.max_calibration_value = sensor_object.max_calibration_value
        sensor_object.min_calibration_value = sensor_object.max_calibration_value


    sensors[sensor_name] = sensor_object.to_dict()




    print(sensor_object.to_dict())
    sensors[sensor_name] = sensor_object.to_dict();

print(sensors)

# Dateipfad für die JSON-Datei
sensors_file_path = os.path.join(os.getcwd() + "/bin/sensors.json")

# Schreiben der sensor_instances in die JSON-Datei
with open(sensors_file_path, "w") as file:
    json.dump(sensors, file, indent=4)

print("Sensor data has been updated.")