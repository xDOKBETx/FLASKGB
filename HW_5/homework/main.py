from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from passlib.context import CryptContext
from pydantic import BaseModel
from starlette.staticfiles import StaticFiles
import uvicorn

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Модель данных для ввода нового пользователя


class UserIn(BaseModel):
    name: str
    email: str
    password: str

# Модель данных для вывода пользователя


class User(BaseModel):
    id: int
    name: str
    email: str

# Модель данных для хранения пользователя с хешированным паролем


class UserDB(UserIn):
    hashed_password: str


users = []

# Функция для хеширования пароля


def get_password_hash(password):
    return pwd_context.hash(password)

# Функция для проверки пароля


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# Маршрут для добавления нового пользователя


@app.post('/add_user')
def add_user(user: UserIn):
    for u in users:
        if u.email == user.email:
            raise HTTPException(
                status_code=400, detail="Email already registered")
    hashed_password = get_password_hash(user.password)
    new_user = UserDB(**user.dict(), hashed_password=hashed_password)
    users.append(new_user)
    return {"message": "User added successfully"}

# Маршрут для вывода списка пользователей в виде HTML


@app.get('/users', response_class=HTMLResponse)
async def user_list(request: Request):
    return templates.TemplateResponse('user_list.html', {'request': request, 'users': users})

# Запуск приложения
if __name__ == '__main__':
    uvicorn.run(app, host="127.0.0.1", port=8000)
