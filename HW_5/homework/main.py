from flask import Flask, request, jsonify, render_template
from dataclasses import dataclass
from typing import List

app = Flask(__name__)


@dataclass
class User:
    id: int
    name: str
    email: str
    password: str


users: List[User] = []


def is_valid_email(email):
    # Простая проверка на валидность email, можно использовать более сложные методы
    return '@' in email


@app.route('/add_user', methods=['POST'])
def add_user():
    try:
        data = request.get_json()

        if not data or 'name' not in data or 'email' not in data or 'password' not in data:
            return jsonify({'error': 'Missing required fields'}), 400

        new_id = len(users) + 1
        new_user = User(
            id=new_id, name=data['name'], email=data['email'], password=data['password'])
        users.append(new_user)

        return jsonify({'message': 'User added successfully'}), 201

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/update_user/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    try:
        data = request.get_json()

        if not data or 'name' not in data or 'email' not in data or 'password' not in data:
            return jsonify({'error': 'Missing required fields'}), 400

        user_to_update = next(
            (user for user in users if user.id == user_id), None)

        if user_to_update is None:
            return jsonify({'error': 'User not found'}), 404

        user_to_update.name = data['name']
        user_to_update.email = data['email']
        user_to_update.password = data['password']

        return jsonify({'message': 'User updated successfully'}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/delete_user/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    try:
        user_to_delete = next(
            (user for user in users if user.id == user_id), None)

        if user_to_delete is None:
            return jsonify({'error': 'User not found'}), 404

        users.remove(user_to_delete)

        return jsonify({'message': 'User deleted successfully'}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/users', methods=['GET'])
def user_list():
    return render_template('user_list.html', users=users)


if __name__ == '__main__':
    app.run(debug=True, port=5000)

