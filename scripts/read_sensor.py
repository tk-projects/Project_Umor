import os
import sys
import time
import threading

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
# Add the parent directory to the sys.path
sys.path.append(parent_dir)

from classes.humidity_sensor import humidity_sensor
from functions.get_sensor import get_sensor

# Global variable to control the loop
running = True

def read_sensor(sensor_id=None, cycle_time =0.5):
    global running
    print(f"Reading sensor with ID: {sensor_id}")
    sensor = get_sensor(sensor_id)
    if sensor:
        try:
            while running:
                data = sensor.read()  # Assuming read() is the method to get sensor data
                time.sleep(cycle_time)
        except KeyboardInterrupt:
            print("Aborted by user using KeyboardInterrupt.")


def listen_for_abort():
    global running
    input("Press Enter to abort...\n")
    running = False

if __name__ == "__main__":
    # Check if arguments are passed
    if len(sys.argv) > 1:
        # Parse sensor_id from command line arguments
        sensor_id = int(sys.argv[1])  # Convert the argument to an integer
        # Start the sensor reading in a separate thread
        sensor_thread = threading.Thread(target=read_sensor, args=(sensor_id,))
        sensor_thread.start()
        
        # Start the abort listening function in the main thread
        listen_for_abort()

        # Wait for the sensor thread to finish
        sensor_thread.join()
    else:
        print("Please provide a sensor_id as an argument.")
