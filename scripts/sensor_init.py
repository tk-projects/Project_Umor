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


sensor_10 = humidity_sensor(10,0,'Sensor_1.0',1,1,'%', 20461, 9951)
sensor_12 = humidity_sensor(11,0,'Sensor_1.1',1,1,'%',0,0);

sensor_group_1 = sensor_group(1, [10, 11],'Prototype Salam','Michendorf','Salam')

sensor_cluster_1 = sensor_cluster(1, [1, 2],'Prototype Salam','Michendorf','Salam')

group_dict = {};
sensor_dict= {};


for i in range(0, len(sensor_cluster_1.groups)):
    group_ob = sensor_cluster_1.groups[i];
    group_dict[group_ob.name] = group_ob.to_dict();

    for j in range(0,len(group_ob.sensors)):
        sensor_obj = group_ob.sensors[j];
        sensor_dict[sensor_obj.name] = sensor_obj.to_dict();

print(sensor_dict)