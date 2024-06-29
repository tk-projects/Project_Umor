import os
import sqlite3
import sys
from datetime import datetime

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
# Add the parent directory to the sys.path
sys.path.append(parent_dir)

from functions.load_sensor_json import load_sensor_json

# Create the SQL directory if it doesn't exist
os.makedirs('SQL', exist_ok=True)

# Get the absolute path to the current directory
current_dir = os.path.dirname(os.path.abspath(__file__))
# Path to the database file in the SQL directory
db_path = os.path.join(current_dir, '..', 'SQL', 'sensor_data.db')

# Database credentials (for consistency, but not used in SQLite)
hostname = 'localhost'
username = 'user'
password = 'password'
database = 'sensor_data'

def create_table(sensor_data):
    try:
        conn = sqlite3.connect(db_path)
        c = conn.cursor()

        # Construct the SQL query to create table with dynamic columns
        columns = ['id INTEGER PRIMARY KEY AUTOINCREMENT', 'timestamp DATETIME DEFAULT CURRENT_TIMESTAMP']
        for sensor_name in sensor_data:
            columns.append(f"{sensor_name} REAL")

        # Join the columns into the CREATE TABLE statement
        columns_str = ", ".join(columns)
        create_table_query = f"CREATE TABLE IF NOT EXISTS humidity_data ({columns_str})"

        # Execute the query to create the table
        c.execute(create_table_query)

        conn.commit()
        conn.close()
        print("Table created successfully.")

    except sqlite3.Error as e:
        print(f"SQLite error: {e}")

def insert_data(sensor_data):
    try:
        conn = sqlite3.connect(db_path)
        c = conn.cursor()

        # Get the current timestamp
        current_timestamp = datetime.now()

        # Prepare the list of column names based on sensor_data keys
        column_names = [key for key in sensor_data.keys()]

        # Prepare the list of values in the same order as column_names
        values = [sensor_data[key] for key in column_names]

        # Construct the INSERT query dynamically
        columns_str = ", ".join(column_names)
        placeholders = ", ".join(["?"] * len(column_names))
        insert_query = f"INSERT INTO humidity_data (timestamp, {columns_str}) VALUES (?, {placeholders})"

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

    # Create table if not exists with dynamic columns based on sensor_data
    create_table(sensor_data)

    # Insert data into the table
    insert_data(sensor_data)

if __name__ == '__main__':
    main()
