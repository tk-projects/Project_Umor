import sqlite3
import os

# Define the path to your SQLite database file
db_path = os.path.join(os.path.dirname(__file__), '..', 'SQL', 'sensor_data.db')

def print_database():
    try:
        # Connect to the SQLite database
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Execute a query to fetch all rows from the humidity_data table
        cursor.execute('SELECT * FROM humidity_data')
        rows = cursor.fetchall()

        # Print fetched data
        for row in rows:
            print(row)

    except sqlite3.Error as e:
        print(f"SQLite error: {e}")

    finally:
        # Close the database connection
        if conn:
            conn.close()

if __name__ == "__main__":
    # Call the function to print the database content
    print_database()
