from classes.humidity_sensor import humidity_sensor
from functions.save_sensor_data import save_sensor_data
from flask import Flask, render_template
import sqlite3
import os
import json
import time

app = Flask(__name__, template_folder='templates')

# Load sensor configuration
sensors_file_path = os.path.join(os.getcwd(), 'bin', 'sensors.json')
print("Loading Sensor Data from: ", sensors_file_path)

with open(sensors_file_path, "r") as json_file:
    sensor_json = json.load(json_file)

sensors = {}
for sensor_name, sensor_data in sensor_json.items():
    sensors[sensor_name] = humidity_sensor(sensor_data["sensor_id"], sensor_data["adc_channel"], sensor_data["name"], sensor_data["unit"], sensor_data["max_calibration_value"], sensor_data["min_calibration_value"])
    print("  • Sensor", sensor_data["sensor_id"], "| Channel:", sensor_data["adc_channel"], "| max value: ", sensor_data["max_calibration_value"], "| min value:", sensor_data["min_calibration_value"], "|")

# Function to fetch data from the database
def fetch_data_from_db():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(current_dir, '..', 'SQL', 'sensor_data.db')
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM humidity_data')
    rows = cursor.fetchall()
    conn.close()
    return rows

# Function to update sensor data
def update_sensor_data():
    humidity = sensors["sensor_1"].read()
    save_sensor_data(sensors["sensor_1"].name, humidity)  # Update DB

# Route for the homepage
@app.route('/')
def index():
    update_sensor_data()  # Update sensor data
    rows = fetch_data_from_db()
    return render_template('index.html', rows=rows)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
