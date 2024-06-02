from flask import Flask, render_template
import sqlite3
import os

app = Flask(__name__)

@app.route('/')
def index():
    # Get the absolute path to the current directory
    current_dir = os.path.dirname(os.path.abspath(__file__))

    # Path to the database file
    db_path = os.path.join(current_dir, '..', 'SQL', 'sensor_data.db')


    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM humidity_data')
    rows = cursor.fetchall()
    conn.close()
    return render_template('/home/tk/Umor/Project_Umor/functions/templates/index.html', rows=rows)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)