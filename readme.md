# User Management Service

## 🚀 Назначение сервиса
Микросервис для управления пользователями и их ресурсами в системе. Основные функции:
- Регистрация пользователей и аутентификация (JWT)
- Управление балансом пользователей
- Отзыв токенов безопасности
- Управление скриптами проектов (CRUD операции)

## 🏷 Архитектура и зависимости

### Технологический стек
- **Backend**: Django 4.2 + DRF 3.15
- **Аутентификация**: JWT (djangorestframework-simplejwt)
- **Документация**: OpenAPI 3.0 (drf-spectacular)
- **База данных**: PostgreSQL
- **Другие зависимости**: psycopg2, python-dotenv

### Взаимодействие с системой
- **Используемые внешние сервисы**: PostgreSQL

### Подготовка
1. Клонируйте репозиторий:
```bash
git clone https://github.com/miet-lambda/user_service.git
cd user_service
```
2. Создайте и активируйте виртуальное окружение:
```bash
python -m venv venv
source venv/bin/activate  # для Linux/Mac
venv\Scripts\activate  # для Windows
```
3. Установите зависимости:
```bash
pip install -r requirements.txt
```
4. Примените миграции базы данных:
```bash
python manage.py migrate
```

## 🛠 Запуск сервиса

### Требования
- Python 3.9+
- PostgreSQL 12+
- Установленные зависимости: `pip install -r requirements.txt`

### Варианты запуска

#### Локальный запуск
```bash
python manage.py runserver
```

### Настройка окружения
Создайте файл `.env` в корне проекта:
```
SECRET_KEY=ваш_секретный_ключ
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

DB_NAME=имя_вашей_бд
DB_USER=ваш_пользователь
DB_PASSWORD=ваш_пароль
DB_HOST=127.0.0.1
DB_PORT=5432
```

## 📚 API Документация
Схема API: `/api/schema/`
Swagger UI: `/api/schema/swagger-ui/`
ReDoc: `/api/schema/redoc/`

## 🧪 Тестирование
```bash
python manage.py test
```

