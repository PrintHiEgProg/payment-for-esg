# Используем официальный образ Python
FROM python:3.9-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Устанавливаем переменные окружения для Python
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Копируем зависимости
COPY requirements.txt .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь проект (кроме указанного в .dockerignore)
COPY . .

# Открываем порт, на котором работает приложение
EXPOSE 7270

# Запускаем приложение с загрузкой .env файла
CMD ["sh", "-c", "python -m dotenv -f .env run uvicorn main:app --host 0.0.0.0 --port 7270"]