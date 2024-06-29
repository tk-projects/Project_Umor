from flask import Flask, render_template, request
import sqlite3
import os
import json

app = Flask(__name__, template_folder='templates')

# Load sensor configuration from JSON file
def load_sensor_config():
    sensors_file_path = os.path.join(os.getcwd(), 'bin', 'sensors.json')
    try:
        with open(sensors_file_path, "r") as json_file:
            sensor_json = json.load(json_file)
    except Exception as e:
        print(f"Error loading sensor configuration: {e}")
        return {}
    return sensor_json

@app.route('/')
def index():
    # Fetch data from the database
    current_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(current_dir, 'SQL', 'sensor_data.db')

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM humidity_data')
    rows = cursor.fetchall()
    conn.close()

    # Load sensor configuration
    sensor_json = load_sensor_config()

    # Prepare sensors dictionary
    sensors = {}
    for sensor_name, sensor_data in sensor_json.items():
        sensor_id = sensor_data["sensor_id"]
        sensors[sensor_id] = {
            "name": sensor_data["name"],
            "adc_channel": sensor_data["adc_channel"],
            "unit": sensor_data["unit"],
            "min_calibration_value": sensor_data["min_calibration_value"],
            "max_calibration_value": sensor_data["max_calibration_value"],
            "sensor_group": sensor_data["sensor_group"],
            "sensor_cluster": sensor_data["sensor_cluster"]
        }

    return render_template('index.html', rows=rows, sensors=sensors)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
