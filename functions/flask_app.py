import os
import sqlite3
import subprocess
from flask import Flask, render_template, request
from functions.load_sensor_json import load_sensor_json
from functions.get_cpu_temperature import get_cpu_temperature
from functions.update_sensor_data import update_sensor_data
from functions.update_database import update_database
from functions.get_sensor import get_sensor

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

    # Generate sensor characteristics data
    sensor_characteristics = load_sensor_json()

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

    return timestamps, data_by_sensor, sensor_characteristics

@app.route('/')
def index():
    timestamps, sensor_data, sensor_characteristics = fetch_all_sensor_data()
    cpu_temperature = get_cpu_temperature()  # Get CPU temperature
    sensor_online = is_sensor_online()  # Check if sensor is online
    print("Sensor_by_date is:",sensor_data)
    return render_template('index.html', timestamps=timestamps, sensor_data=sensor_data,sensor_characteristics =sensor_characteristics,
                           cpu_temperature=cpu_temperature, sensor_online=sensor_online)

# Route to handle restart action
@app.route('/restart', methods=['POST'])
def restart_pi():
    try:
        os.system('sudo reboot')  # Command to restart Raspberry Pi
        return 'Raspberry Pi is restarting...', 200
    except Exception as e:
        return f'Error restarting Raspberry Pi: {str(e)}', 500

# Route to handle update now action
@app.route('/update_sensor_now', methods=['POST'])
def update_sensor_now():
    # get all awailable sensors:
    sensor_data = load_sensor_json()

    # Get sensor IDs
    sensor_ids = [sensor_info["sensor_id"] for sensor_info in sensor_data.values()]
    print("Sensors loaded by flask app:",sensor_ids)
    sensors = []
    for sensor_id in sensor_ids:
        sensor = get_sensor(sensor_id)
        if sensor:
            sensors.append(sensor)
    print("All sensors:", sensors)

    print("Now updating sensor database ...")

    readings = update_sensor_data(sensors)
    update_database(readings)

    timestamps, sensor_data, sensor_characteristics = fetch_all_sensor_data()
    cpu_temperature = get_cpu_temperature()  # Get CPU temperature
    sensor_online = is_sensor_online()  # Check if sensor is online
    return render_template('index.html', timestamps=timestamps, sensor_data=sensor_data,sensor_characteristics =sensor_characteristics,
                           cpu_temperature=cpu_temperature, sensor_online=sensor_online)
    




if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
