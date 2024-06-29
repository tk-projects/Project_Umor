from flask import Flask, render_template
import sqlite3
import os

app = Flask(__name__, template_folder='templates')

# Function to fetch data from the database for Sensor1.0 and Sensor1.1
def fetch_sensor_data():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(current_dir, 'SQL', 'sensor_data.db')

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('SELECT timestamp, humidity_value FROM humidity_data WHERE sensor_name IN (?, ?) ORDER BY timestamp DESC',
                   ('Sensor1.0', 'Sensor1.1'))
    rows = cursor.fetchall()
    conn.close()

    sensor_data = {
        'Sensor1.0': {'timestamps': [], 'humidities': []},
        'Sensor1.1': {'timestamps': [], 'humidities': []}
    }

    for row in rows:
        sensor_name = 'Sensor1.0' if row[0] == 'Sensor1.1' else 'Sensor1.0'
        sensor_data[sensor_name]['timestamps'].append(row[0])
        sensor_data[sensor_name]['humidities'].append(row[1])

    return sensor_data

@app.route('/')
def index():
    sensor_data = fetch_sensor_data()
    return render_template('index.html', sensor_data=sensor_data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
