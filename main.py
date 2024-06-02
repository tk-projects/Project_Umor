from classes.humidity_sensor import humidity_sensor
from functions.save_sensor_data import save_sensor_data
from flask import Flask, render_template
import sqlite3
import os
import json
import time
import threading

app = Flask(__name__, template_folder='templates')

# Load sensor configuration
sensors_file_path = os.path.join(os.getcwd(), 'bin', 'sensors.json')
print("Loading Sensor Data from:", sensors_file_path)

try:
    with open(sensors_file_path, "r") as json_file:
        sensor_json = json.load(json_file)
except Exception as e:
    print(f"Error loading sensor configuration: {e}")
    exit(1)

# Initialize sensors
sensors = {}
for sensor_name, sensor_data in sensor_json.items():
    sensors[sensor_name] = humidity_sensor(
        sensor_data["sensor_id"], sensor_data["adc_channel"],
        sensor_data["name"], sensor_data["unit"],
        sensor_data["max_calibration_value"], sensor_data["min_calibration_value"]
    )
    print(f"  • Sensor {sensor_data['sensor_id']} | Channel: {sensor_data['adc_channel']} | "
          f"max value: {sensor_data['max_calibration_value']} | min value: {sensor_data['min_calibration_value']}")

# Function to fetch data from the database
def fetch_data_from_db():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(current_dir, 'SQL', 'sensor_data.db')
    try:
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM humidity_data')
            rows = cursor.fetchall()
        return rows
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return []

# Function to update sensor data
def update_sensor_data():
    try:
        humidity = sensors["sensor_1"].read()
        save_sensor_data(sensors["sensor_1"].name, humidity)  # Update DB
    except Exception as e:
        print(f"Error updating sensor data: {e}")

# Background thread to update sensor data every n seconds
def sensor_data_updater():
    sampling_rate = 60
    while True:
        last_datapoint = get_last_datapoint()
        if last_datapoint:
            last_timestamp = datetime.datetime.strptime(last_datapoint, '%Y-%m-%d %H:%M:%S')
            current_timestamp = datetime.datetime.now()
            time_difference = (current_timestamp - last_timestamp).total_seconds()
            if time_difference >= sampling_rate-1:
                update_sensor_data()
        else:
            update_sensor_data()  # No data in the database, insert the first datapoint
        time.sleep(sampling_rate)

def get_last_datapoint():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(current_dir, 'SQL', 'sensor_data.db')
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('SELECT timestamp FROM humidity_data ORDER BY timestamp DESC LIMIT 1')
    row = cursor.fetchone()
    conn.close()
    if row:
        return row[0]
    return None

# Route for the homepage
@app.route('/')
def index():
    rows = fetch_data_from_db()
    return render_template('index.html', rows=rows)

if __name__ == '__main__':
    # Start the background thread
    updater_thread = threading.Thread(target=sensor_data_updater)
    updater_thread.daemon = True
    updater_thread.start()
    
    # Run the Flask application
    app.run(host='0.0.0.0', port=8080, debug=True)
