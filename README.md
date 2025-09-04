# Test_task / Тестовое_задание

## English

### Description
This project is a FastAPI backend for managing users, departments, and files.  
It includes authentication, role-based access control, and CRUD operations.
The API is documented with Swagger/OpenAPI. All endpoints have docstrings.

### Features
- User management (CRUD, role-based access)
- Department management
- File upload/download (pending testing)
- PostgreSQL database integration
- Async SQLAlchemy
- JWT authentication

### Quick Start
Build and run the project with Docker:

```
docker compose up --build
```
### Usage

Access API docs: http://127.0.0.1:8000/docs

## Русский

### Описание

Этот проект — бэкенд на FastAPI для управления пользователями, отделами и файлами.
Включает аутентификацию, контроль доступа на основе ролей и операции CRUD.
Документация API предоставлена через Swagger/OpenAPI. Все эндпоинты снабжены docstring.

### Возможности

Управление пользователями (CRUD, контроль доступа по ролям)

Управление отделами

Загрузка и скачивание файлов (тестирование в процессе)

Интеграция с PostgreSQL

Асинхронный SQLAlchemy

JWT-аутентификация

### Быстрый запуск
```
docker compose up --build
```

### Использование

Доступ к документации API: http://127.0.0.1:8000/docs
