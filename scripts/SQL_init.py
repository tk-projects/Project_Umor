import os
import sqlite3
import sys
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

def create_table():
    try:
        conn = sqlite3.connect(db_path)
        c = conn.cursor()

        # Create the humidity_data table with separate columns for each sensor
        c.execute('''CREATE TABLE IF NOT EXISTS humidity_data (
                         id INTEGER PRIMARY KEY AUTOINCREMENT,
                         timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                         sensor_1 REAL,
                         sensor_2 REAL
                     )''')

        conn.commit()
        conn.close()
        print("Table created successfully.")

    except sqlite3.Error as e:
        print(f"SQLite error: {e}")

def insert_data(sensor_data):
    try:
        conn = sqlite3.connect(db_path)
        c = conn.cursor()

        # Example data to insert
        for sensor_name, humidity_value in sensor_data.items():
            # Assuming sensor names are 'Sensor_1' and 'Sensor_2'
            if sensor_name == 'Sensor_1':
                c.execute("INSERT INTO humidity_data (sensor_1) VALUES (?)", (humidity_value,))
            elif sensor_name == 'Sensor_2':
                c.execute("INSERT INTO humidity_data (sensor_2) VALUES (?)", (humidity_value,))

        conn.commit()
        conn.close()
        print("Data inserted successfully.")

    except sqlite3.Error as e:
        print(f"SQLite error: {e}")

def main():
    # Create table if not exists
    create_table()

    # Get sensor data
    sensor_data = load_sensor_json()

    # Insert data into the table
    insert_data(sensor_data)

if __name__ == '__main__':
    main()
