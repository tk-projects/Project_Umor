import sqlite3
import os

# Define the path to your SQLite database file
db_path = os.path.join(os.path.dirname(__file__), '..', 'SQL', 'sensor_data.db')

def print_database():

    try:
        # Connect to the SQLite database
        print("connecting to sql db, with path:",db_path)
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Execute a query to fetch all rows from the humidity_data table
        cursor.execute('SELECT * FROM humidity_data')
        
        # Fetch column names
        columns = [description[0] for description in cursor.description]
        
        # Print column headers
        print(columns)
        
        # Print fetched data
        rows = cursor.fetchall()
        for row in rows:
            print(row)

    except sqlite3.Error as e:
        print(f"SQLite error: {e}")

    finally:
        # Close the database connection
        if conn:
            conn.close()


print_database()
