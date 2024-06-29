import sqlite3
import os

# Define the path to your SQLite database file
db_path = os.path.join(os.path.dirname(__file__), '..', 'SQL', 'sensor_data.db')

def reset_database():

    try:
        # Connect to the SQLite database
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Execute SQL command to delete all rows from the humidity_data table
        cursor.execute('DELETE FROM humidity_data')
        
        # Commit the transaction
        conn.commit()
        
        print("Database reset successful.")

    except sqlite3.Error as e:
        print(f"SQLite error: {e}")

    finally:
        # Close the database connection
        if conn:
            conn.close()

if __name__ == "__main__":
    # Call the function to reset the database
    reset_database()
