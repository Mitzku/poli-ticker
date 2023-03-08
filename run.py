from flask import Flask, request, render_template, url_for
import sqlite3

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/")
def home():
    return render_template('home.html')

@app.route("/test")
def template():
    return render_template('test.html')

@app.route("/politiker")
def politiker():
    name_filter = request.args.get('name')
    conn = get_db_connection()

    if not name_filter:
        data = conn.execute(f"SELECT * FROM df_politiker_selenium").fetchall()
    else:
        data = conn.execute(f"SELECT * FROM df_politiker_selenium WHERE vorname LIKE '%{name_filter}%'").fetchall()
        
    conn.close()
    return render_template('politiker.html', data=data)

@app.route("/abstimmungen")
def abstimmungen():
    name_filter = request.args.get('name')
    conn = get_db_connection()

    if not name_filter:
        data = conn.execute(f"SELECT * FROM df_abstimmungen_selenium").fetchall()
    else:
        data = conn.execute(f"SELECT * FROM df_abstimmungen_selenium WHERE Abstimmungsthema LIKE '%{name_filter}%'").fetchall()
        
    conn.close()
    return render_template('abstimmungen.html', data=data)

@app.route("/abstimmungsverhalten", methods=['POST'])
def abstimmungsverhalten():
    bundestags_id = request.form['bundestags_id']
    conn = get_db_connection()
    query = f"WITH abs AS (SELECT * FROM df_abstimmungen_selenium WHERE bundestags_id = {bundestags_id}), pol AS (SELECT * FROM df_politiker_selenium WHERE bundestags_id = {bundestags_id}) SELECT * FROM abs LEFT JOIN pol ON abs.bundestags_id = pol.bundestags_id"
    data = conn.execute(query).fetchall()
    conn.close()
    return render_template('abstimmungsverhalten.html', data=data)


#Checks if the run.py file has executed directly and not imported
if __name__ == '__main__':
    app.run(debug=True)


