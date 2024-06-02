import sqlite3

def save_sensor_data(sensor_name, humidity_value):
    conn = sqlite3.connect('sensor_data.db')
    c = conn.cursor()
    
    c.execute("INSERT INTO humidity_data (sensor_name, humidity_value) VALUES (?, ?)", (sensor_name, humidity_value))
    
    conn.commit()
    conn.close()

# Beispiel: Speichern eines Sensormesswerts
save_sensor_data("sensor_1", 45.3)
