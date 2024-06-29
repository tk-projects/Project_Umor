import os
import sys
import time
import threading
import json

# Global variable to control the loop
running = True

def read_sensor_from_json(file_path, cycle_time=0.5):
    global running
    try:
        with open(file_path, 'r') as file:
            sensor_data = json.load(file)
        
        sensor_name = sensor_data.get("name")
        adc_channel = sensor_data.get("adc_channel")
        min_calibration_value = sensor_data.get("min_calibration_value")
        max_calibration_value = sensor_data.get("max_calibration_value")

        print(f"Reading sensor from JSON file: {file_path}")
        print(f"Sensor Name: {sensor_name}")
        print(f"ADC Channel: {adc_channel}")
        print(f"Min Calibration Value: {min_calibration_value}")
        print(f"Max Calibration Value: {max_calibration_value}")

    except FileNotFoundError:
        print(f"JSON file {file_path} not found.")
    except json.JSONDecodeError:
        print(f"Error decoding JSON file {file_path}.")



if __name__ == "__main__":
    # Check if arguments are passed
    if len(sys.argv) > 1:
        # Parse sensor_id from command line arguments
        sensor_id = int(sys.argv[1])  # Convert the argument to an integer
        # Start the sensor reading in a separate thread
        
    else:
        print("Please provide a sensor_id as an argument.")