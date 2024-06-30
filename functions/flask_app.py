import os
import sqlite3
from flask import Flask, render_template
from functions.load_sensor_json import load_sensor_json

app = Flask(__name__, template_folder='templates')

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
    print("sensor_names:",sensor_names)

    # Prepare the query to fetch data for all sensors
    columns = ['timestamp'] + sensor_names
    columns_str = ', '.join(columns)
    cursor.execute(f'SELECT {columns_str} FROM humidity_data ORDER BY timestamp DESC')
    rows = cursor.fetchall()
    conn.close()

    # Organize data by sensor_name
    data_by_sensor = {sensor_name: [] for sensor_name in sensor_names}
    for row in rows:
        timestamp = row[0]
        for i, sensor_name in enumerate(sensor_names):
            data_by_sensor[sensor_name].append({
                'timestamp': timestamp,
                'humidity_value': row[i + 1]
            })

    return data_by_sensor

@app.route('/')
def index():
    sensor_data = fetch_all_sensor_data()
    return render_template('index.html', sensor_data=sensor_data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
