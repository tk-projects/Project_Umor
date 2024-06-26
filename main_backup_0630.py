import os
import sqlite3
import sys
import threading
from datetime import datetime
from time import sleep
from flask import Flask, render_template
from functions.load_sensor_json import load_sensor_json
from functions.get_sensor import get_sensor

app = Flask(__name__, template_folder='templates')


def insert_data(sensor_readings):
    parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    # Add the parent directory to the sys.path
    sys.path.append(parent_dir)

    # Path to the database file in the SQL directory
    db_path = os.path.join(parent_dir, 'SQL', 'sensor_data.db')

    print("Parent Directory:", parent_dir)
    print("Database Path:", db_path)
    try:
        print("starting connection")
        conn = sqlite3.connect(db_path)
        print("connection done")
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

        print("insert_query",insert_query)
        # Execute the query to insert data
        c.execute(insert_query, (current_timestamp,) + tuple(values))
        print("executed")
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
            for sensor in sensors:
                try:
                    sensor_readings[sensor.name] = sensor.read()
                except Exception as e:
                    print(f"Error reading sensor {sensor.name}: {e}")
                    sensor_readings[sensor.name] = 0.0

            # Insert data into the table
            insert_data(sensor_readings)

        except Exception as e:
            print(f"Unexpected error: {e}")

        # Sleep for sampling_rate seconds before next update
        sleep(sampling_rate)

def fetch_all_sensor_data():
    parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    # Add the parent directory to the sys.path
    sys.path.append(parent_dir)

    # Path to the database file in the SQL directory
    db_path = os.path.join(parent_dir, 'SQL', 'sensor_data.db')

    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT sensor_name, timestamp, humidity_value FROM humidity_data ORDER BY timestamp DESC')
        rows = cursor.fetchall()
        conn.close()

        # Organize data by sensor_name
        sensor_data = {}
        for row in rows:
            sensor_name = row[0]
            if sensor_name not in sensor_data:
                sensor_data[sensor_name] = {
                    'timestamps': [],
                    'humidities': []
                }
            sensor_data[sensor_name]['timestamps'].append(row[1])
            sensor_data[sensor_name]['humidities'].append(row[2])

        return sensor_data

    except sqlite3.Error as e:
        print(f"SQLite error: {e}")
        return {}

@app.route('/')
def index():
    sensor_data = fetch_all_sensor_data()
    return render_template('index.html', sensor_data=sensor_data)

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
        updater_thread = threading.Thread(target=sensor_data_updater, args=(sensors,))
        updater_thread.daemon = True
        updater_thread.start()

        # Run the Flask app
        app.run(host='0.0.0.0', port=8080, debug=True)

    except Exception as e:
        print(f"Unexpected error in main thread: {e}")

if __name__ == '__main__':
    main()
