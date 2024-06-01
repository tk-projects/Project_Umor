from  classes.humidity_sensor import humidity_sensor
import os
import json

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

for i in range(1,number_of_sensors):
    sensor_idx = i;
    sensor_name = f"sensor_{i}";
    sensor_channel = sensor_channel_mapping.get(sensor_name,"Sensor nicht gefunden. Prüfe die sensor_channel_mapping.json Datei im Ordner /bin/ !")
    sensors[sensor_name] = humidity_sensor(1,sensor_name,sensor_channel,"% Lufteuchte")

print(sensors)

# Dateipfad für die JSON-Datei
sensors_jason = "/bin/sensor_instances.json"

# Schreiben der sensor_instances in die JSON-Datei
with open(json_file_path, "w") as file:
    json.dump(sensors, file, indent=4)