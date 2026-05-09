from flask import Flask, request, redirect, render_template_string
import psycopg2
import os

app = Flask(__name__)

def get_db():
    return psycopg2.connect(
        host=os.environ.get('DB_HOST', 'db'),
        database=os.environ.get('DB_NAME', 'tododb'),
        user=os.environ.get('DB_USER', 'admin'),
        password=os.environ.get('DB_PASSWORD', 'secret123')
    )

def init_db():
    conn = get_db()
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS todos (
            id SERIAL PRIMARY KEY,
            task VARCHAR(200) NOT NULL,
            done BOOLEAN DEFAULT FALSE
        )
    ''')
    conn.commit()
    cur.close()
    conn.close()

HTML = '''
<!DOCTYPE html>
<html>
<head>
    <title>Todo App</title>
    <style>
        body { font-family: Arial; max-width: 600px; margin: 50px auto; background: #1a1a2e; color: white; }
        h1 { color: #e94560; }
        input { padding: 10px; width: 70%; border-radius: 5px; border: none; }
        button { padding: 10px 20px; background: #e94560; color: white; border: none; border-radius: 5px; cursor: pointer; }
        ul { list-style: none; padding: 0; }
        li { background: rgba(255,255,255,0.1); padding: 10px; margin: 5px 0; border-radius: 5px; }
    </style>
</head>
<body>
    <h1>🐳 Docker Todo App</h1>
    <p>Built by Nilesh | Flask + PostgreSQL + Docker Compose</p>
    <form method="POST" action="/add">
        <input name="task" placeholder="Enter a task..." required>
        <button type="submit">Add Task</button>
    </form>
    <ul>
        {% for todo in todos %}
        <li>{{ todo[1] }}</li>
        {% endfor %}
    </ul>
</body>
</html>
'''

@app.route('/')
def index():
    conn = get_db()
    cur = conn.cursor()
    cur.execute('SELECT * FROM todos')
    todos = cur.fetchall()
    cur.close()
    conn.close()
    return render_template_string(HTML, todos=todos)

@app.route('/add', methods=['POST'])
def add():
    task = request.form['task']
    conn = get_db()
    cur = conn.cursor()
    cur.execute('INSERT INTO todos (task) VALUES (%s)', (task,))
    conn.commit()
    cur.close()
    conn.close()
    return redirect('/')

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000, debug=True)