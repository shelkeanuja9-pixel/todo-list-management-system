from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

def connect_db():
    return sqlite3.connect("database.db")

@app.route('/')
def home():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        task TEXT,
        status TEXT DEFAULT 'Pending'
    )
    """)

    cursor.execute("SELECT * FROM tasks")
    tasks = cursor.fetchall()
    conn.close()

    return render_template('index.html', tasks=tasks)

@app.route('/add', methods=['POST'])
def add():
    task = request.form['task']
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO tasks (task) VALUES (?)", (task,))
    conn.commit()
    conn.close()
    return redirect('/')

@app.route('/delete/<int:id>')
def delete(id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tasks WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return redirect('/')

@app.route('/complete/<int:id>')
def complete(id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE tasks SET status='Completed' WHERE id=?", (id,)
    )
    conn.commit()
    conn.close()
    return redirect('/')

@app.route('/update/<int:id>', methods=['POST'])
def update(id):
    task = request.form['task']
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("UPDATE tasks SET task=? WHERE id=?", (task, id))
    conn.commit()
    conn.close()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
