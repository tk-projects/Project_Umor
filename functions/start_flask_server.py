from flask import Flask, render_template
import sqlite3

app = Flask(__name__)

def get_sensor_data():
    # Path to the database file in the SQL directory
    db_path = os.path.join('SQL', 'sensor_data.db')
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("SELECT * FROM humidity_data")
    data = c.fetchall()
    conn.close()
    return data

@app.route('/')
def index():
    data = get_sensor_data()
    return render_template('index.html', data=data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)