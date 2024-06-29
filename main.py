import os
import sqlite3
import sys
from datetime import datetime

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
# Add the parent directory to the sys.path
sys.path.append(parent_dir)

from functions.load_sensor_json import load_sensor_json
from classes.humidity_sensor import humidity_sensor

# Create the SQL directory if it doesn't exist
os.makedirs('SQL', exist_ok=True)

# Get the absolute path to the current directory
current_dir = os.path.dirname(os.path.abspath(__file__))
# Path to the database file in the SQL directory
db_path = os.path.join(current_dir, '..', 'SQL', 'sensor_data.db')

def sanitize_column_name(name):
    """Replace invalid characters in column names with underscores."""
    return name.replace('.', '_')

def create_table(sensor_data):
    try:
        conn = sqlite3.connect(db_path)
        c = conn.cursor()

        # Prepare the dynamic part of the SQL for columns, sanitizing the names
        columns = ', '.join([f"{sanitize_column_name(key)} REAL" for key in sensor_data.keys()])

        # Create the humidity_data table with separate columns for each sensor
        create_table_query = f'''
        CREATE TABLE IF NOT EXISTS humidity_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            {columns}
        )
        '''

        print("Create Table Query:", create_table_query)  # Debugging line

        c.execute(create_table_query)
        conn.commit()
        conn.close()
        print("Table created successfully.")

    except sqlite3.Error as e:
        print(f"SQLite error: {e}")

def insert_data(sensor_data, sensor_readings):
    try:
        conn = sqlite3.connect(db_path)
        c = conn.cursor()

        # Get the current timestamp
        current_timestamp = datetime.now()

        # Prepare the list of column names based on sensor_data keys
        column_names = [sanitize_column_name(key) for key in sensor_data.keys()]

        # Use the actual sensor readings as values
        values = [sensor_readings.get(key, 0.0) for key in sensor_data.keys()]

        # Construct the INSERT query dynamically
        columns_str = ", ".join(column_names)
        placeholders = ", ".join(["?"] * len(column_names))
        insert_query = f"INSERT INTO humidity_data (timestamp, {columns_str}) VALUES (?, {placeholders})"

        print("Insert Query:", insert_query)  # Debugging line
        print("Values:", (current_timestamp,) + tuple(values))  # Debugging line

        # Execute the query to insert data
        c.execute(insert_query, (current_timestamp,) + tuple(values))

        conn.commit()
        conn.close()
        print("Data inserted successfully.")

    except sqlite3.Error as e:
        print(f"SQLite error: {e}")

def main():
    # Get sensor data
    sensor_data = load_sensor_json()

    # Create table if not exists
    create_table(sensor_data)

    # Initialize sensors
    sensors = {}
    for sensor_name, sensor_info in sensor_data.items():
        sensor_id = sensor_info["sensor_id"]
        sensors[sensor_id] = humidity_sensor(
            sensor_info["sensor_id"], sensor_info["adc_channel"],
            sensor_info["name"], sensor_info["sensor_group"], sensor_info["sensor_cluster"], sensor_info["unit"],
            sensor_info["max_calibration_value"], sensor_info["min_calibration_value"]
        )

    # Fetch sensor readings
    sensor_readings = {}
    for sensor_id, sensor in sensors.items():
        try:
            sensor_readings[sensor_id] = sensor.read()
        except Exception as e:
            print(f"Error reading sensor {sensor_id}: {e}")
            sensor_readings[sensor_id] = 0.0

    # Insert data into the table
    insert_data(sensor_data, sensor_readings)

if __name__ == '__main__':
    main()
