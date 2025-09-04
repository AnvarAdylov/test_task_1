# Test_task / Тестовое_задание

## English

### Description
This project is a FastAPI backend for managing users, departments, and files.  
It includes authentication, role-based access control, and CRUD operations.

### Features
- User management (CRUD, role-based access)
- Department management
- File upload/download (pending testing)
- PostgreSQL database integration
- Async SQLAlchemy
- JWT authentication

### Installation
```
git clone https://github.com/AnvarAdylov/test_task_1.git
cd project
python -m venv venv
source venv/bin/activate  # Linux / Mac
venv\Scripts\activate     # Windows
pip install -r requirements.txt
```
Running
uvicorn app.main:app --reload

Usage

Access API docs: http://127.0.0.1:8000/docs

## Русский

### Описание

Этот проект — бэкенд на FastAPI для управления пользователями, отделами и файлами.
Включает аутентификацию, контроль доступа на основе ролей и операции CRUD.

### Возможности

Управление пользователями (CRUD, контроль доступа по ролям)

Управление отделами

Загрузка и скачивание файлов (тестирование в процессе)

Интеграция с PostgreSQL

Асинхронный SQLAlchemy

JWT-аутентификация

### Установка
```
git clone https://github.com/AnvarAdylov/test_task_1.git
cd project
python -m venv venv
source venv/bin/activate  # Linux / Mac
venv\Scripts\activate     # Windows
pip install -r requirements.txt
```
Запуск
uvicorn app.main:app --reload

Использование

Доступ к документации API: http://127.0.0.1:8000/docs
