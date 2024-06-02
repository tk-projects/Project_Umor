# SQL Database generation
import os
import sqlite3

# Create the SQL directory if it doesn't exist
os.makedirs('SQL', exist_ok=True)

# Path to the database file in the SQL directory
db_path = os.path.join('SQL', 'sensor_data.db')

# Verbindung zur Datenbank herstellen
conn = sqlite3.connect(db_path)
c = conn.cursor()

# Tabelle erstellen
c.execute('''CREATE TABLE IF NOT EXISTS humidity_data (
                 id INTEGER PRIMARY KEY AUTOINCREMENT,
                 timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                 sensor_name TEXT,
                 humidity_value REAL
             )''')

# Verbindung schließen
conn.commit()
conn.close()