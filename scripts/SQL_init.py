import os
import sqlite3
from datetime import datetime
import sys

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
# Add the parent directory to the sys.path (if necessary)
sys.path.append(parent_dir)

from functions.load_sensor_json import load_sensor_json

# Create the SQL directory if it doesn't exist
os.makedirs(os.path.join(parent_dir, 'SQL'), exist_ok=True)

# Path to the database file in the SQL directory
db_path = os.path.join(parent_dir, 'SQL', 'sensor_data.db')

print("Parent Directory:", parent_dir)
print("Database Path:", db_path)

def create_table(sensor_data):
    try:
        conn = sqlite3.connect(db_path)
        c = conn.cursor()

        # Prepare the dynamic part of the SQL for columns
        columns = ', '.join([f"{key.replace('.', '_')} REAL" for key in sensor_data.keys()])

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
        print("Table created successfully.")

    except sqlite3.Error as e:
        print(f"SQLite error during table creation: {e}")
    finally:
        conn.close()

def insert_data(sensor_data):
    try:
        conn = sqlite3.connect(db_path)
        c = conn.cursor()

        # Get the current timestamp
        current_timestamp = datetime.now()

        # Prepare the list of column names based on sensor_data keys
        column_names = [key.replace('.', '_') for key in sensor_data.keys()]

        # Use 0 as the value for each sensor
        values = [0.0] * len(column_names)

        # Construct the INSERT query dynamically
        columns_str = ", ".join(['timestamp'] + column_names)
        placeholders = ", ".join(["?"] * (len(column_names) + 1))
        insert_query = f"INSERT INTO humidity_data ({columns_str}) VALUES ({placeholders})"

        print("Insert Query:", insert_query)  # Debugging line
        print("Values:", (current_timestamp,) + tuple(values))  # Debugging line

        # Execute the query to insert data
        c.execute(insert_query, (current_timestamp,) + tuple(values))

        conn.commit()
        print("Data inserted successfully.")

    except sqlite3.Error as e:
        print(f"SQLite error during data insertion: {e}")
    finally:
        conn.close()

def main():
    try:
        # Get sensor data
        sensor_data = load_sensor_json()

        # Create table if not exists
        create_table(sensor_data)

        # Insert data into the table
        insert_data(sensor_data)

    except Exception as e:
        print(f"Unexpected error in main thread: {e}")

if __name__ == '__main__':
    main()
