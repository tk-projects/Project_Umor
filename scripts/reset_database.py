import sqlite3
import os

# Get the absolute path to the current directory
current_dir = os.path.dirname(os.path.abspath(__file__))

# Path to the database file
db_path = os.path.join(current_dir, 'SQL', 'sensor_data.db')

# Connect to the SQLite database
conn = sqlite3.connect(db_path)
c = conn.cursor()

# Delete all records from the humidity_data table
c.execute('DELETE FROM humidity_data')

# Commit changes and close the connection
conn.commit()
conn.close()

print("Database reset successfully.")