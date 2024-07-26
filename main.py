import os
import sqlite3
import sys
import threading
from datetime import datetime
from time import sleep
from functions.load_sensor_json import load_sensor_json
from functions.get_sensor import get_sensor
import argparse

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__)))
sys.path.append(parent_dir)

# Path to the database file in the SQL directory
db_path = os.path.join(parent_dir, 'SQL', 'sensor_data.db')

def insert_data(sensor_readings):
    parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__)))
    sys.path.append(parent_dir)

    # Path to the database file in the SQL directory
    db_path = os.path.join(parent_dir, 'SQL', 'sensor_data.db')
    try:
        print("connecting to sql db, with path:", db_path)
        conn = sqlite3.connect(db_path)
        c = conn.cursor()

        # Get the current timestamp
        current_timestamp = datetime.now()

        # Prepare the list of column names based on sensor_data keys
        column_names = list(sensor_readings.keys())

        # Prepare the values list based on sensor_readings
        values = [sensor_readings[sensor_name] for sensor_name in column_names]

        # Construct the INSERT query dynamically
        columns_str = ", ".join(['timestamp'] + column_names)
        placeholders = ", ".join(["?"] * (len(column_names) + 1))
        insert_query = f"INSERT INTO humidity_data ({columns_str}) VALUES ({placeholders})"

        c.execute(insert_query, (current_timestamp,) + tuple(values))
        conn.commit()
        conn.close()
        print("Data inserted successfully.")

    except sqlite3.Error as e:
        print(f"SQLite error: {e}")

def sensor_data_updater(sensors):
    sampling_rate = 600  # Update every 600 seconds
    while True:
        try:
            # Fetch sensor readings
            sensor_readings = {}
            sensor_vals = []
             
            for sensor in sensors:
                try:
                    for i in range(0,30):
                        sensor_vals.append(sensor.read())
                        print(sensor.name,":",sensor.read())
                        sleep(1)
                    
                    sensor_average = sum(sensor_vals)/len(sensor_vals)
                    print("SENSOR AVERAGE IS:",sensor_average)
                    sensor_readings[sensor.name] = sensor_average
                except Exception as e:
                    print(f"Error reading sensor {sensor.name}: {e}")
                    sensor_readings[sensor.name] = 0.0

            # Insert data into the table
            insert_data(sensor_readings)

        except Exception as e:
            print(f"Unexpected error: {e}")

        # Sleep for sampling_rate seconds before next update
        sleep(sampling_rate)

def main():
    parser = argparse.ArgumentParser(description="Sensor Data Updater and Server")
    parser.add_argument('--port', type=int, default=8080, help='Port number to run the server on')
    args = parser.parse_args()

    port = args.port
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

        # Ensure the sensor data updater thread runs only once
        if not threading.current_thread().name == "MainThread":
            return

        # Start the sensor data updater thread
        updater_thread = threading.Thread(target=sensor_data_updater, args=(sensors,))
        updater_thread.daemon = True
        updater_thread.start()

        # Import and run the Flask app
        from functions.flask_app import app
        app.run(host='0.0.0.0', port=port, debug=True, use_reloader=False)

    except Exception as e:
        print(f"Unexpected error in main thread: {e}")

if __name__ == '__main__':
    main()
