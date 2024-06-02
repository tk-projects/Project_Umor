from flask import Flask, render_template
import sqlite3
import os

app = Flask(__name__)

@app.route('/')
def index():
    # Get the absolute path to the current directory
    current_dir = os.path.dirname(os.path.abspath(__file__))

    # Path to the database file
    db_path = os.path.join(current_dir, 'SQL', 'sensor_data.db')

    # Connect to the SQLite database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Fetch data from the database
    cursor.execute('SELECT * FROM humidity_data')
    rows = cursor.fetchall()

    # Close the database connection
    conn.close()

    # Pass the data to the template and render it
    return render_template('/templates/sensor_data.html', rows=rows)

if __name__ == '__main__':
    # Run the Flask application
    app.run(host='0.0.0.0', port=80, debug=True)
