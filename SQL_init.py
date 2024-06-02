# SQL Database generation
import os
import sqlite3

# Create the SQL directory if it doesn't exist
os.makedirs('SQL', exist_ok=True)

# Path to the database file in the SQL directory
db_path = os.path.join('SQL', 'sensor_data.db')

# Verbindung zur Datenbank herstellen
conn = sqlite3.connect(db_path)

# Establish connection to MySQL database
conn = mysql.connector.connect(
    host="umor",  # Replace with your MySQL host
    user="tk",  # Replace with your MySQL username
    password="1234",  # Replace with your MySQL password
    database="sensor_data"  # Replace with the name of your MySQL database
)

c = conn.cursor()

# Tabelle erstellen
c.execute('''CREATE TABLE IF NOT EXISTS humidity_data (
                 id INTEGER PRIMARY KEY AUTOINCREMENT,
                 timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                 sensor_name TEXT,
                 humidity_value REAL
             )''')


# Example data to insert
sensor_name = 'sensor_1'
humidity_value = 0

# Insert data into the table
c.execute("INSERT INTO humidity_data (sensor_name, humidity_value) VALUES (?, ?)", (sensor_name, humidity_value))


# Verbindung schließen
conn.commit()
conn.close()