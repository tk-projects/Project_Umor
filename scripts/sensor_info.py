import os
import sys
import json


parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
# Add the parent directory to the sys.path
sys.path.append(parent_dir)

from functions.get_sensor import get_sensor

# Global variable to control the loop
running = True

def sensor_info(sensor_id):
    global running
    sensor_data = get_sensor(sensor_id)
    
    sensor_name = sensor_data.name
    min_calibration_value = sensor_data.min_calibration_value
    max_calibration_value = sensor_data.max_calibration_value

    print(f"Sensor Name: {sensor_name}")
    print(f"Min Calibration Value: {min_calibration_value}")
    print(f"Max Calibration Value: {max_calibration_value}")


if __name__ == "__main__":
    # Check if arguments are passed
    if len(sys.argv) > 1:
        # Parse sensor_id from command line arguments
        sensor_id = int(sys.argv[1])  # Convert the argument to an integer
        sensor_info(sensor_id)
    else:
        print("Please provide a sensor_id as an argument.")