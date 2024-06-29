import sqlite3
import sys
import os

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
# Add the parent directory to the sys.path
sys.path.append(parent_dir)

current_directory = os.path.dirname(__file__)

# Path to your SQLite database file
db_path = os.path.join(current_directory, "..", "SQL", "sensor_data.db")


def view_database():
    try:
        # Connect to the SQLite database
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Example query: Fetch all rows from the humidity_data table
        cursor.execute('SELECT * FROM humidity_data')
        rows = cursor.fetchall()

        # Print fetched data (for verification purposes)
        for row in rows:
            print(row)

    except sqlite3.Error as e:
        print(f"SQLite error: {e}")

    finally:
        # Close the database connection
        if conn:
            conn.close()

# Call the function to view the database
view_database()
