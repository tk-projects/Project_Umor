import os
import sqlite3
import subprocess
from flask import Flask, render_template, jsonify
from functions.load_sensor_json import load_sensor_json
from functions.get_cpu_temperature import get_cpu_temperature
from main import sensor_data_updater

import logging

logging.basicConfig(level=logging.DEBUG)
app.logger.setLevel(logging.DEBUG)


app = Flask(__name__, template_folder=os.path.join(os.path.dirname(__file__), '..', 'templates'))

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

# Route to handle restart action
@app.route('/restart', methods=['POST'])
def restart_pi():
    try:
        os.system('sudo reboot')  # Command to restart Raspberry Pi
        return 'Raspberry Pi is restarting...', 200
    except Exception as e:
        return f'Error restarting Raspberry Pi: {str(e)}', 500

# Update sensor data now
@app.route('/update_sensors', methods=['POST'])
def update_sensors():
    try:
        # Call the sensor_data_updater function directly
        print("try to call sensor_data_updater function")
        sensor_data_updater()
        print("function called")
        return jsonify({'message': 'Sensors updated and data inserted successfully.'}), 200
    except Exception as e:
        # Log the error and return a JSON error message
        app.logger.error(f'Error updating sensors: {e}')
        return jsonify({'error': f'Error updating sensors: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
