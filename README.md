# Homework 1 — FastAPI Calculator (Windows)

Простой API-калькулятор на FastAPI для темы **«Введение в бэкенд. Асинхронность в Python»**.

## Запуск на Windows (PowerShell)

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python app\main.py
```

## Запуск на Windows (CMD)

```cmd
py -m venv .venv
.venv\Scripts\activate.bat
pip install -r requirements.txt
python app\main.py
```

> Если Execution Policy блокирует `Activate.ps1`, откройте PowerShell от администратора и выполните:
>
> `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`

## Что реализовано

1. **Базовые операции** (`+`, `-`, `*`, `/`) через `POST /calculate/binary`.
2. **Создание/сохранение текущего выражения** через `POST /expression`.
3. **Просмотр текущего выражения** через `GET /expression`.
4. **Выполнение текущего выражения** через `POST /expression/execute`.
5. **Вычисление сложного выражения строкой** через `POST /calculate/expression`.

## Примеры запросов (Windows PowerShell)

### 1) Бинарная операция

```powershell
curl.exe -X POST http://127.0.0.1:8000/calculate/binary ^
-H "Content-Type: application/json" ^
-d "{\"a\":10,\"op\":\"*\",\"b\":5}"
```

### 2) Сохранить выражение

```powershell
curl.exe -X POST http://127.0.0.1:8000/expression ^
-H "Content-Type: application/json" ^
-d "{\"expression\": \"(2+3)*4 + (10-2)/(6-4)\"}"
```

### 3) Посмотреть текущее выражение

```powershell
curl.exe http://127.0.0.1:8000/expression
```

### 4) Выполнить текущее выражение

```powershell
curl.exe -X POST http://127.0.0.1:8000/expression/execute
```

### 5) Вычислить выражение сразу

```powershell
curl.exe -X POST http://127.0.0.1:8000/calculate/expression `
  -H "Content-Type: application/json" `
  -d '{"expression": "(2+3)*4 + (10-2)/(6-4)"}'
```

## Документация

После запуска:
- Swagger UI: <http://127.0.0.1:8000/docs>
- ReDoc: <http://127.0.0.1:8000/redoc>
