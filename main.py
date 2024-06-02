from flask import Flask, render_template
import sqlite3
import os
import time

app = Flask(__name__, template_folder='templates')
update_flag = False  # Flag to signal database update

# Function to fetch data from the database
def fetch_data_from_db():
    # Get the absolute path to the current directory
    current_dir = os.path.dirname(os.path.abspath(__file__))

    # Path to the database file
    db_path = os.path.join(current_dir, '..', 'SQL', 'sensor_data.db')

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM humidity_data')
    rows = cursor.fetchall()
    conn.close()
    return rows

# Route for the homepage
@app.route('/')
def index():
    if update_flag:
        update_flag = False  # Reset the flag
        rows = fetch_data_from_db()  # Fetch updated data from the database
    else:
        rows = fetch_data_from_db()  # Fetch data from the database

    return render_template('index.html', rows=rows)

# Function to periodically check for database updates
def check_for_updates():
    while True:
        # Your main script logic goes here
        # Measure sensor data and update the database
        # For demonstration purposes, let's simulate database updates every time
        # You should replace this with your actual logic

        humidity = sensors["sensor_1"].read()  # Read sensor data
        save_sensor_data(sensors["sensor_1"].name, humidity)  # Update database

        # Signal the Flask app to refresh the webpage
        update_flag = True

        # Sleep for a short duration before checking for updates again
        time.sleep(10)  # Adjust this value as needed

# Start checking for updates
if __name__ == '__main__':
    # Start a thread to check for updates
    check_updates_thread = threading.Thread(target=check_for_updates)
    check_updates_thread.start()

    # Run the Flask app
    app.run(host='0.0.0.0', port=8080, debug=True)
