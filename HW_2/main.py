from flask import Flask, render_template, request, redirect, make_response

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    """Обработчик для главной страницы, где пользователь вводит имя и электронную почту."""
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']

        # Создание куки с данными пользователя
        response = make_response(redirect('/welcome'))
        response.set_cookie('user_name', name)
        response.set_cookie('user_email', email)
        return response

    return render_template('index.html')


@app.route('/welcome')
def welcome():
    """Обработчик для страницы приветствия, где отображается имя пользователя."""
    user_name = request.cookies.get('user_name')
    if user_name:
        return render_template('welcome.html', user_name=user_name)
    else:
        return redirect('/')


@app.route('/exit')
def exit():
    """Обработчик для выхода из приложения, который удаляет куки и перенаправляет на страницу ввода данных."""
    # Удаление куки пользователя
    response = make_response(redirect('/'))
    response.delete_cookie('user_name')
    response.delete_cookie('user_email')
    return response


if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)
