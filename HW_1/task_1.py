# Задание №1
# 📌 Напишите простое веб-приложение на Flask, которое будет выводить на экран текст "Hello, World!".

from flask import Flask

app = Flask(__name__)


@app.route('/')
def index():
    return 'Hello, World!'


if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)
