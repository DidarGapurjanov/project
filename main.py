from fastapi import FastAPI, Request, Form, Depends
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from starlette.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from pages.router import router as pages_router
from products.router import router as product_router
from auth.schemas import UserRead, UserCreate
from auth.base_config import auth_backend, fastapi_users
import uvicorn
from redis import asyncio as aioredis

app = FastAPI(
    title="UrbanGizmo"
)
app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

app.include_router(pages_router, prefix="")
app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth",
    tags=["Auth"],
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["Auth"],
)

app.include_router(product_router)


# Событие запуска приложения
@app.on_event("startup")
async def startup_event():
    # Подключение к Redis
    redis = aioredis.from_url("redis://localhost", encoding="utf8", decode_responses=True)
    # Инициализация кэширования с использованием Redis
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
    # Сохранение соединения с Redis в состоянии приложения
    app.state.redis = redis


# Событие завершения работы приложения
@app.on_event("shutdown")
async def shutdown_event():
    # Закрытие соединения с Redis
    await app.state.redis.close()


# Маршрут для отображения страницы регистрации
@app.get("/register", response_class=HTMLResponse)
async def get_register(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})


# Маршрут для обработки данных регистрации
@app.post("/register", response_class=HTMLResponse)
async def post_register(request: Request, username: str = Form(...), email: str = Form(...), password: str = Form(...)):
    # Ваш код для обработки данных регистрации, например, создание пользователя
    return templates.TemplateResponse("register.html", {"request": request, "message": "User registered successfully!"})


# Маршрут для отображения страницы входа
@app.get("/login", response_class=HTMLResponse)
async def get_login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

"""
# Маршрут для обработки данных входа
@app.post("/login", response_class=HTMLResponse)
async def post_login(request: Request, email: str = Form(...), password: str = Form(...), user=Depends(fastapi_users.current_user)):
    # Проверка данных входа и аутентификация пользователя
    if user:
        return templates.TemplateResponse("login.html", {"request": request, "message": "Login successful!"})
    else:
        return templates.TemplateResponse("login.html", {"request": request, "message": "Invalid email or password"})
"""
if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8080,
        reload=True,
    )
