import os
import sqlite3
import sys


# Create the SQL directory if it doesn't exist
os.makedirs('SQL', exist_ok=True)

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
# Add the parent directory to the sys.path
sys.path.append(parent_dir)

# Get the absolute path to the current directory
current_dir = os.path.dirname(os.path.abspath(__file__))
# Path to the database file in the SQL directory
db_path = os.path.join(current_dir, '..', 'SQL', 'sensor_data.db')

from functions.load_sensor_json import load_sensor_json

# Database credentials (for consistency, but not used in SQLite)
hostname = 'localhost'
username = 'user'
password = 'password'
database = 'sensor_data'

# Connect to SQLite database (credentials not used)
conn = sqlite3.connect(db_path)
c = conn.cursor()

# Create the humidity_data table
c.execute('''CREATE TABLE IF NOT EXISTS humidity_data (
                 id INTEGER PRIMARY KEY AUTOINCREMENT,
                 timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                 sensor_name TEXT,
                 humidity_value REAL
             )''')

# Example data to insert
sensor_name = 'sensor_1'
humidity_value = 0

# Get sensor data
sensor_data = load_sensor_json()

for sensor_name in sensor_data:

    # Insert data into the table
    c.execute("INSERT INTO humidity_data (sensor_name, humidity_value) VALUES (?, ?)", (sensor_name, humidity_value))

# Commit changes and close the connection
conn.commit()
conn.close()