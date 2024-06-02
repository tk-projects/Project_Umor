import threading
from  classes.humidity_sensor import humidity_sensor
from functions.save_sensor_data import save_sensor_data
from flask import Flask, render_template
import sqlite3
import os
import json
import time

app = Flask(__name__, template_folder='templates')

# Function to run the Flask app
def run_flask_app():
    app.run(host='0.0.0.0', port=8080, debug=True)

# Function for the main script
def main():
    sensors_file_path = os.path.join(os.getcwd() + "/bin/sensors.json")
    print("Loading Sensor Data from: ", sensors_file_path)

    with open(sensors_file_path, "r") as json_file:
        sensor_json = json.load(json_file)

    print("________________________________________________________________________________________________________")
    print("________________________________________________________________________________________________________\n")
    print("Importing Sensor Data:")
    dauer = 22
    for _ in range(dauer):
        print(".", end="", flush=True)
        time.sleep(0.05)

    print("\n")

    sensors = {}

    for sensor_name, sensor_json in sensor_json.items():
        sensors[sensor_name] = humidity_sensor(sensor_json["sensor_id"], sensor_json["adc_channel"], sensor_json["name"], sensor_json["unit"], sensor_json["max_calibration_value"], sensor_json["min_calibration_value"])
        print("  • Sensor",sensor_json["sensor_id"], "| Channel:", sensor_json["adc_channel"], "| max value: ", sensor_json["max_calibration_value"], "| min value:",sensor_json["min_calibration_value"],"|")

    print("\nSensor class data: ", sensors)

    print("Sensor 1 measurement:")
    while True:
        humidity = sensors["sensor_1"].read()
        save_sensor_data(sensors["sensor_1"].name, humidity) # Update DB
        time.sleep(10)

# Start Flask app in a separate thread
flask_thread = threading.Thread(target=run_flask_app)
flask_thread.start()

# Run the main script
main()
