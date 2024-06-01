from  classes.humidity_sensor import humidity_sensor
import json

sensor = humidity_sensor(1, 0)
print(sensor)

#sensor.calibrate();


number_of_sensors = 1

# Load sensor mappings:
with open("bin\sensor_channel_mapping.json", "r") as file:
        sensor_channel_mapping = json.load(file)

print(sensor_channel_mapping)