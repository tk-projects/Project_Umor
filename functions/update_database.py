import os
import sqlite3
import sys
from datetime import datetime

def update_database(sensor_readings):
    parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__)))
    sys.path.append(parent_dir)

    # Path to the database file in the SQL directory
    db_path = os.path.join(parent_dir,'..', 'SQL', 'sensor_data.db')
    try:
        print("connecting to sql db, with path:", db_path)
        conn = sqlite3.connect(db_path)
        c = conn.cursor()

        # Get the current timestamp
        current_timestamp = datetime.now()

        # Prepare the list of column names based on sensor_data keys
        column_names = list(sensor_readings.keys())

        # Prepare the values list based on sensor_readings
        values = [sensor_readings[sensor_name] for sensor_name in column_names]

        # Construct the INSERT query dynamically
        columns_str = ", ".join(['timestamp'] + column_names)
        placeholders = ", ".join(["?"] * (len(column_names) + 1))
        insert_query = f"INSERT INTO humidity_data ({columns_str}) VALUES ({placeholders})"

        c.execute(insert_query, (current_timestamp,) + tuple(values))
        conn.commit()
        conn.close()
        print("Data inserted successfully.")

    except sqlite3.Error as e:
        print(f"SQLite error: {e}")