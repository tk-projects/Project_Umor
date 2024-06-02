import sqlite3

# Get the absolute path to the current directory
current_dir = os.path.dirname(os.path.abspath(__file__))

# Path to the database file
db_path = os.path.join(current_dir, '..', 'SQL', 'sensor_data.db')

# Connect to SQLite database
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Execute SQL query
cursor.execute('SELECT * FROM humidity_data')
rows = cursor.fetchall()

# Print the results
for row in rows:
    print(row)

# Close the cursor and connection
cursor.close()
conn.close()
