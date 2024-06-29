# Read sensor data script for debugging
import os
import sys


parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
# Add the parent directory to the sys.path
sys.path.append(parent_dir)

from classes.humidity_sensor import humidity_sensor
from functions.get_sensor import get_sensor



def read_sensor(sensor_id=None,sensor_name=None):
    print(sensor_id)
    sensor =  get_sensor(sensor_id)
    print(sensor)