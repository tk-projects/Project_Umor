# Sensor Init
import sys
import os

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
# Add the parent directory to the sys.path
sys.path.append(parent_dir)

from  classes.humidity_sensor import humidity_sensor
from  classes.sensor_group import sensor_group
from classes.sensor_cluster import sensor_cluster
import json

# Create sensor objects
sensor_10 = humidity_sensor(10,0,'Sensor_1.0',1,1,'%', 20461, 9951)
sensor_11 = humidity_sensor(11,0,'Sensor_1.1',1,1,'%',0,0);

# Create a sensor group with the sensors
sensor_group_1 = sensor_group(1, [sensor_10, sensor_11],'Prototype Salam','Michendorf','Salam')


# Create a sensor cluster with the group
sensor_cluster_1 = sensor_cluster(1, [sensor_group_1],'Prototype Salam','Michendorf','Salam')

# Initialize dictionaries to hold group and sensor data
group_dict = {}
sensor_dict = {}

# Iterate over the groups in the cluster
for group in sensor_cluster_1.groups:
    # Convert group object to dictionary and add to group_dict
    group_dict[group.name] = group.to_dict()

    # Iterate over the sensors in the group
    for sensor in group.sensors:
        # Convert sensor object to dictionary and add to sensor_dict
        sensor_dict[sensor.name] = sensor.to_dict()

print(sensor_dict)