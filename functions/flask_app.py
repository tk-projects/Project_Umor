import os
import sqlite3
import subprocess
from flask import Flask, render_template, jsonify
from functions.load_sensor_json import load_sensor_json
from functions.get_cpu_temperature import get_cpu_temperature
from datetime import datetime
from functions import get_sensor

import logging

logging.basicConfig(level=logging.DEBUG)



app = Flask(__name__, template_folder=os.path.join(os.path.dirname(__file__), '..', 'templates'))


def insert_data(sensor_readings):
    try:
        conn = sqlite3.connect(db_path)
        c = conn.cursor()

        current_timestamp = datetime.now()
        column_names = list(sensor_readings.keys())
        values = [sensor_readings[sensor_name] for sensor_name in column_names]

        columns_str = ", ".join(['timestamp'] + column_names)
        placeholders = ", ".join(["?"] * (len(column_names) + 1))
        insert_query = f"INSERT INTO humidity_data ({columns_str}) VALUES ({placeholders})"

        c.execute(insert_query, (current_timestamp,) + tuple(values))
        conn.commit()
        conn.close()
        print("Data inserted successfully.")
    except sqlite3.Error as e:
        print(f"SQLite error: {e}")
        raise

def get_sensor_readings():
    # Load sensor data and initialize sensors
    sensor_data = load_sensor_json()
    sensor_ids = [sensor_info["sensor_id"] for sensor_info in sensor_data.values()]
    sensors = [get_sensor(sensor_id) for sensor_id in sensor_ids if get_sensor(sensor_id)]
    
    sensor_readings = {}
    for sensor in sensors:
        try:
            sensor_readings[sensor.name] = sensor.read()
        except Exception as e:
            print(f"Error reading sensor {sensor.name}: {e}")
            sensor_readings[sensor.name] = 0.0
    return sensor_readings

# Function to check if sensor is online (example implementation)
def is_sensor_online():
    # Replace with your logic to check sensor status
    return True  # For example, always returning True here

# Function to fetch data from the database for all sensors
def fetch_all_sensor_data():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(current_dir, "..", "SQL", "sensor_data.db")
    print("Flask app is connecting now")

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Load sensor data from JSON to get the sensor names
    sensor_data = load_sensor_json()
    sensor_names = list(sensor_data.keys())

    # Prepare the query to fetch data for all sensors
    columns = ['timestamp'] + sensor_names
    columns_str = ', '.join(columns)
    cursor.execute(f'SELECT {columns_str} FROM humidity_data ORDER BY timestamp ASC')
    rows = cursor.fetchall()
    conn.close()

    # Organize data by sensor_name
    data_by_sensor = {sensor_name: [] for sensor_name in sensor_names}
    timestamps = []
    for row in rows:
        timestamp = row[0]
        timestamps.append(timestamp)
        for i, sensor_name in enumerate(sensor_names):
            data_by_sensor[sensor_name].append(row[i + 1])

    return timestamps, data_by_sensor

@app.route('/')
def index():
    timestamps, sensor_data = fetch_all_sensor_data()
    cpu_temperature = get_cpu_temperature()  # Get CPU temperature
    sensor_online = is_sensor_online()  # Check if sensor is online
    return render_template('index.html', timestamps=timestamps, sensor_data=sensor_data,
                           cpu_temperature=cpu_temperature, sensor_online=sensor_online)

@app.route('/update_sensors', methods=['POST'])
def update_sensors():
    try:
        print("Fetching sensor readings...")
        sensor_readings = get_sensor_readings()
        print("Inserting data into database...")
        insert_data(sensor_readings)
        return jsonify({'message': 'Sensors updated and data inserted successfully.'}), 200
    except Exception as e:
        print(f"Error in update_sensors: {e}")
        return jsonify({'error': f'Failed to update sensors: {str(e)}'}), 500


# Route to handle restart action
@app.route('/restart', methods=['POST'])
def restart_pi():
    try:
        os.system('sudo reboot')  # Command to restart Raspberry Pi
        return 'Raspberry Pi is restarting...', 200
    except Exception as e:
        return f'Error restarting Raspberry Pi: {str(e)}', 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
