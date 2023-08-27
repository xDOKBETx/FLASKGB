from pydantic import BaseModel

# Модель данных для создания нового продукта
class ProductCreate(BaseModel):
    title: str  # Название продукта
    description: str  # Описание продукта
    price: float  # Цена продукта

# Модель данных для получения информации о продукте
class ProductRetrieve(BaseModel):
    id: int  # Идентификатор продукта
    title: str  # Название продукта
    description: str  # Описание продукта
    price: float  # Цена продукта

# Модель данных для создания нового пользователя
class UserCreate(BaseModel):
    first_name: str  # Имя пользователя
    last_name: str  # Фамилия пользователя
    email: str  # Электронная почта пользователя
    password: str  # Пароль пользователя

# Модель данных для получения информации о пользователе
class UserRetrieve(BaseModel):
    id: int  # Идентификатор пользователя
    first_name: str  # Имя пользователя
    last_name: str  # Фамилия пользователя
    email: str  # Электронная почта пользователя

# Модель данных для создания нового заказа
class OrderCreate(BaseModel):
    user_id: int  # Идентификатор пользователя
    product_id: int  # Идентификатор продукта
    order_status: str  # Статус заказа

# Модель данных для получения информации о заказе
class OrderRetrieve(BaseModel):
    id: int  # Идентификатор заказа
    user_id: int  # Идентификатор пользователя
    product_id: int  # Идентификатор продукта
    order_date: str  # Дата заказа
    order_status: str  # Статус заказа
