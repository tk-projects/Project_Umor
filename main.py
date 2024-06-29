import os
import sqlite3
import sys
from datetime import datetime

# Assuming this import loads sensor data as a dictionary where keys are sensor names or IDs
from functions.load_sensor_json import load_sensor_json
from classes.humidity_sensor import humidity_sensor

# Function to create a sanitized column name
def sanitize_column_name(name):
    return name.replace('.', '_')

# Function to create the database table if it doesn't exist
def create_table(sensor_data):
    try:
        db_path = os.path.join(os.path.dirname(__file__), 'SQL', 'sensor_data.db')
        conn = sqlite3.connect(db_path)
        c = conn.cursor()

        # Check if the table already exists
        c.execute("SELECT count(*) FROM sqlite_master WHERE type='table' AND name='humidity_data'")
        table_exists = c.fetchone()[0]

        if not table_exists:
            # Prepare the dynamic part of the SQL for columns, sanitizing the names
            columns = ', '.join([f"{sanitize_column_name(key)} REAL" for key in sensor_data.keys()])

            # Create the humidity_data table with separate columns for each sensor
            create_table_query = f'''
            CREATE TABLE humidity_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                {columns}
            )
            '''

            print("Create Table Query:", create_table_query)  # Debugging line

            c.execute(create_table_query)
            conn.commit()
            print("Table created successfully.")
        else:
            print("Table 'humidity_data' already exists. Skipping table creation.")

        conn.close()

    except sqlite3.Error as e:
        print(f"SQLite error: {e}")

# Function to insert sensor data into the database
def insert_data(sensor_data, sensor_readings):
    try:
        db_path = os.path.join(os.path.dirname(__file__), 'SQL', 'sensor_data.db')
        print("db_path:",db_path)
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

# Main function to orchestrate the data retrieval and insertion
def main():
    try:
        # Get sensor data
        sensor_data = load_sensor_json()

        # Create table if not exists
        create_table(sensor_data)

        # Initialize sensors (this assumes you have a class that manages sensor readings)
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
                sensor_readings[sanitize_column_name(sensor_id)] = sensor.read()
            except Exception as e:
                print(f"Error reading sensor {sensor_id}: {e}")
                sensor_readings[sanitize_column_name(sensor_id)] = 0.0

        # Insert data into the table
        insert_data(sensor_data, sensor_readings)

    except Exception as e:
        print(f"Unexpected error: {e}")

if __name__ == '__main__':
    main()
