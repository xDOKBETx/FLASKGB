import os
import sqlite3
import bcrypt
from flask import Flask, render_template, request, g

app = Flask(__name__)

# Путь к файлу базы данных SQLite
db_path = os.path.join(os.path.dirname(__file__), 'data', 'mydatabase.db')

# Создаем подключение к базе данных
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(db_path)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

# Функция для создания таблицы users
def create_table():
    db = get_db()
    cursor = db.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT,
            last_name TEXT,
            email TEXT,
            password TEXT
        )
    ''')
    db.commit()
    cursor.close()

@app.before_request
def before_request():
    create_table()

@app.route('/', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        password = request.form['password']

        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        try:
            db = get_db()
            cursor = db.cursor()
            sql = "INSERT INTO users (first_name, last_name, email, password) VALUES (?, ?, ?, ?)"
            cursor.execute(sql, (first_name, last_name, email, hashed_password))
            db.commit()
            cursor.close()
            return "Registration successful!"
        except Exception as e:
            return str(e)

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
