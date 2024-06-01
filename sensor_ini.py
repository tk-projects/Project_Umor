from  classes.humidity_sensor import humidity_sensor
import os
import json
import pickle

#sensor = humidity_sensor(1, 0)
#print(sensor)

#sensor.calibrate();


number_of_sensors = 1


# Get the current directory of the script
current_directory = os.path.dirname(__file__)

# Specify the path to the JSON file relative to the current directory
json_file_path = os.path.join(os.getcwd() + "/bin/sensor_channel_mapping.json")

# Open and read the JSON file
with open(json_file_path, "r") as file:
    sensor_channel_mapping = json.load(file)

# Create a dictionary to store sensor instances
sensors = {}
print(sensor_channel_mapping)

for i in range(1,number_of_sensors+1):
    sensor_idx = i;
    sensor_name = f"sensor_{i}";
    print(sensor_name)
    sensor_channel = sensor_channel_mapping.get(sensor_name," Error: Sensor nicht gefunden. Prüfe die sensor_channel_mapping.json Datei im Ordner /bin/ !")
    sensors[sensor_name] = humidity_sensor(sensor_idx, sensor_channel, sensor_name, "% Lufteuchte")

print(sensors)

# Dateipfad für die JSON-Datei
sensors_file_path = os.path.join(os.getcwd() + "/bin/sensors.pickle")

# Schreiben der sensor_instances in die JSON-Datei
with open(sensors_file_path, "w") as file:
    pickle.dump(sensors, file)