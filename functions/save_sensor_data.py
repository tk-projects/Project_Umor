import sqlite3
import os

def save_sensor_data(sensor_name, humidity_value):
    # Create the SQL directory if it doesn't exist
    os.makedirs('SQL', exist_ok=True)

    # Path to the database file in the SQL directory
    db_path = os.path.join('SQL', 'sensor_data.db')
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    
    c.execute("INSERT INTO humidity_data (sensor_name, humidity_value) VALUES (?, ?)", (sensor_name, humidity_value))
    
    conn.commit()
    conn.close()
    print("Updated DB with data from",sensor_name, "and value:", humidity_value)

# Beispiel: Speichern eines Sensormesswerts
save_sensor_data("sensor_1", 45.3)
