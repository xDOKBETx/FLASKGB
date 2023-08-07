from flask import Flask, render_template

# Создание экземпляра приложения Flask
app = Flask(__name__)

# Пример данных для категорий товаров
categories = {
    "clothing": "Одежда",
    "shoes": "Обувь",
    "jacket": "Куртки",
}

# Пример данных для товаров в различных категориях
products = {
    "clothing": [
        {"id": 1, "name": "Футболка", "description": "Красная футболка", "price": 500},
        {"id": 2, "name": "Джинсы", "description": "Синие джинсы", "price": 1000},
        {"id": 3, "name": "Платье", "description": "Черное платье", "price": 1500},
    ],
    "shoes": [
        {"id": 4, "name": "Кроссовки", "description": "Белые кроссовки", "price": 800},
        {"id": 5, "name": "Ботинки", "description": "Кожаные ботинки", "price": 1200},
        {"id": 6, "name": "Сандали", "description": "Летние сандали", "price": 600},
    ],
    "jacket": [
        {"id": 7, "name": "Кожаная куртка", "description": "Черная кожаная куртка", "price": 2000},
        {"id": 8, "name": "Дождевик", "description": "Прозрачный дождевик", "price": 300},
        {"id": 9, "name": "Зимнее пальто", "description": "Теплое зимнее пальто", "price": 2500},
    ],
}

# Обработчик маршрута для главной страницы
@app.route('/')
def home():
    return render_template('base.html')

# Обработчик маршрута для страницы категории товаров
@app.route('/category/<category_name>')
def category(category_name):
    if category_name in categories:
        return render_template('category.html', category=categories[category_name], products=products[category_name])
    else:
        return "Категория не найдена"

# Обработчик маршрута для страницы отдельного товара
@app.route('/product/<int:product_id>')
def product(product_id):
    for category_products in products.values():
        for product in category_products:
            if product["id"] == product_id:
                return render_template('product.html', product=product)
    return "Товар не найден"

# Запуск приложения Flask при условии, что скрипт запускается непосредственно (не импортирован)
if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)
