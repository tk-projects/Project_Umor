from flask import Flask, render_template
import sqlite3
import os

app = Flask(__name__, template_folder='templates')

# Function to fetch data from the database for a specific sensor
def fetch_sensor_data(sensor_name):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(current_dir, 'SQL', 'sensor_data.db')

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('SELECT timestamp, humidity_value FROM humidity_data WHERE sensor_name = ?', (sensor_name,))
    rows = cursor.fetchall()
    conn.close()

    timestamps = []
    humidities = []
    for row in rows:
        timestamps.append(row[0])
        humidities.append(row[1])

    return timestamps, humidities

@app.route('/')
def index():
    # List of sensors (replace with your actual sensor names)
    sensors = ['sensor_1', 'sensor_2', 'sensor_3']  # Replace with actual sensor names from your DB

    # Dictionary to store data for each sensor
    sensor_data = {}

    # Fetch data for each sensor
    for sensor_name in sensors:
        timestamps, humidities = fetch_sensor_data(sensor_name)
        sensor_data[sensor_name] = {
            'timestamps': timestamps,
            'humidities': humidities
        }

    return render_template('index.html', sensor_data=sensor_data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
