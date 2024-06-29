import os
import sqlite3
import sys
import json
import time
import threading
import datetime
from flask import Flask, render_template


parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
# Add the parent directory to the sys.path
sys.path.append(parent_dir)

from classes.humidity_sensor import humidity_sensor

# Initialize Flask application
app = Flask(__name__, template_folder='templates')

# Load sensor configuration from JSON file
sensors_file_path = os.path.join(os.getcwd(), 'bin', 'sensors.json')

try:
    with open(sensors_file_path, "r") as json_file:
        sensor_json = json.load(json_file)
except Exception as e:
    print(f"Error loading sensor configuration: {e}")
    exit(1)

# Initialize sensors dictionary
sensors = {}
for sensor_name, sensor_data in sensor_json.items():
    sensor_id = sensor_data["sensor_id"]

    # Create and store instances of humidity_sensor
    sensors[sensor_id] = humidity_sensor(
        sensor_data["sensor_id"], sensor_data["adc_channel"],
        sensor_data["name"], sensor_data["sensor_group"], sensor_data["sensor_cluster"], sensor_data["unit"],
        sensor_data["max_calibration_value"], sensor_data["min_calibration_value"]
    )

# Define path to SQLite database file
current_dir = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(current_dir, 'SQL', 'sensor_data.db')

# Function to fetch all data from the database
def fetch_data_from_db():
    try:
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM humidity_data')
            rows = cursor.fetchall()
        return rows
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return []

# Function to update sensor data for all sensors
def update_sensor_data():
    try:
        # Get current timestamp
        current_timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # Prepare data for insertion
        data_to_insert = [(current_timestamp, sensors[sensor_id].name, sensors[sensor_id].read()) for sensor_id in sensors.keys()]

        # Connect to the database and insert data
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            cursor.executemany("INSERT INTO humidity_data (timestamp, sensor_name, humidity_value) VALUES (?, ?, ?)", data_to_insert)
            conn.commit()

        print("Data inserted successfully.")

    except sqlite3.Error as e:
        print(f"SQLite error: {e}")

# Background thread to update sensor data every n seconds
def sensor_data_updater():
    sampling_rate = 60
    while True:
        update_sensor_data()
        time.sleep(sampling_rate)

# Route for the homepage
@app.route('/')
def index():
    rows = fetch_data_from_db()
    return render_template('index.html', rows=rows)

# Main function to start the application
if __name__ == '__main__':
    # Start the background thread for data updating
    updater_thread = threading.Thread(target=sensor_data_updater)
    updater_thread.daemon = True
    updater_thread.start()

    # Run the Flask application
    app.run(host='0.0.0.0', port=8080, debug=True)
