# Задание №7
# 📌 Написать функцию, которая будет выводить на экран HTML страницу с блоками новостей.
# 📌 Каждый блок должен содержать заголовок новости, краткое описание и дату публикации.
# 📌 Данные о новостях должны быть переданы в шаблон через контекст.

from flask import Flask
from flask import render_template

app = Flask(__name__)

class News:
    def __init__(self, title, description, date):
        self.title = title
        self.description = description
        self.date = date

@app.route('/')
def html_task_7():
    news = [News('Новость', 'Описание', 'Дата'), News('Новость', 'Описание', 'Дата'), News('Новость', 'Описание', 'Дата')]
    return render_template('task_7.html', news=news)


if __name__ == '__main__':
    app.run(debug=True)
