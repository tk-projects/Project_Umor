import os
import sqlite3
import sys
import threading
from datetime import datetime
from time import sleep

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
# Add the parent directory to the sys.path
sys.path.append(parent_dir)

from functions.load_sensor_json import load_sensor_json
from classes.humidity_sensor import humidity_sensor
from functions.save_sensor_data import save_sensor_data
from functions.get_sensor import get_sensor

# Create the SQL directory if it doesn't exist
os.makedirs('SQL', exist_ok=True)

# Get the absolute path to the current directory
current_dir = os.path.dirname(os.path.abspath(__file__))
# Path to the database file in the SQL directory
db_path = os.path.join(current_dir, 'SQL', 'sensor_data.db')

def insert_data(sensor_data, sensor_readings):
    try:
        conn = sqlite3.connect(db_path)
        c = conn.cursor()

        # Get the current timestamp
        current_timestamp = datetime.now()

        # Prepare the list of column names based on sensor_data keys
        column_names = sensor_data.keys()

        # Prepare the values list based on sensor_readings
        values = [sensor_readings[key] if key in sensor_readings else 0.0 for key in sensor_data.keys()]

        # Construct the INSERT query dynamically
        columns_str = ", ".join(['timestamp'] + column_names)
        placeholders = ", ".join(["?"] * (len(sensor_data) + 1))
        insert_query = f"INSERT INTO humidity_data ({columns_str}) VALUES ({placeholders})"

        print("Insert Query:", insert_query)  # Debugging line
        print("Values:", (current_timestamp,) + tuple(values))  # Debugging line

        # Execute the query to insert data
        c.execute(insert_query, (current_timestamp,) + tuple(values))

        conn.commit()
        conn.close()
        print("Data inserted successfully.")

    except sqlite3.Error as e:
        print(f"SQLite error: {e}")

def sensor_data_updater(sensors):
    sampling_rate = 10  # Update every 10 seconds
    while True:
        try:

            # Fetch sensor readings
            sensor_readings = {}
            for sensor in sensors.items():
                try:
                    sensor_readings[sensor.name] = sensor.read()
                except Exception as e:
                    print(f"Error reading sensor {sensor.name}: {e}")
                    sensor_readings[sensor.name] = 0.0

            # Insert data into the table
            insert_data(sensors, sensor_readings)

        except Exception as e:
            print(f"Unexpected error: {e}")

        # Sleep for sampling_rate seconds before next update
        sleep(sampling_rate)

def main():
    try:
        # Get sensor data
        sensor_data = load_sensor_json()

        # Get sensor IDs
        sensor_ids = [sensor_info["sensor_id"] for sensor_info in sensor_data.values()]
        print(sensor_ids)

        sensors = []
        for sensor_id in sensor_ids:
            sensor = get_sensor(sensor_id)
            if sensor:
                sensors.append(sensor)

        print(sensors)
        
        

        # Start the sensor data updater thread
        updater_thread = threading.Thread(target=sensor_data_updater(sensors))
        updater_thread.daemon = True
        updater_thread.start()

        # Keep the main thread alive
        while True:
            sleep(1)  # Keep the main thread running

    except Exception as e:
        print(f"Unexpected error in main thread: {e}")

if __name__ == '__main__':
    main()
