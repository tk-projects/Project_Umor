from flask import Flask, render_template
import sqlite3
import os

app = Flask(__name__, template_folder='templates')

# Function to fetch data from the database for all sensors
def fetch_all_sensor_data():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(current_dir, "..", "SQL", "sensor_data.db")
    print("Flask app is connecting now")

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('SELECT sensor_name, timestamp, humidity_value FROM humidity_data ORDER BY timestamp DESC')
    rows = cursor.fetchall()
    conn.close()

    # Organize data by sensor_name
    sensor_data = {}
    for row in rows:
        sensor_name = row[0]
        if sensor_name not in sensor_data:
            sensor_data[sensor_name] = {
                'timestamps': [],
                'humidities': []
            }
        sensor_data[sensor_name]['timestamps'].append(row[1])
        sensor_data[sensor_name]['humidities'].append(row[2])

    return sensor_data

@app.route('/')
def index():
    sensor_data = fetch_all_sensor_data()
    return render_template('index.html', sensor_data=sensor_data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
