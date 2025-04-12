# FastAPI Payment Service with YooKassa

## Описание проекта

Сервис для обработки платежей через YooKassa с генерацией QR-кодов. Проект предоставляет API для:
- Создания платежей
- Генерации QR-кодов для оплаты
- Проверки статуса платежей

## Технологии

- Python 3.9+
- FastAPI
- YooKassa SDK
- QRCode generation
- Docker

## Установка и запуск

### Локальная разработка

1. Клонируйте репозиторий:
```bash
git clone https://github.com/yourusername/payment-service.git
cd payment-service
```

2. Создайте и активируйте виртуальное окружение:
```bash
python -m venv venv
source venv/bin/activate  # Linux/MacOS
# или 
venv\Scripts\activate  # Windows
```

3. Установите зависимости:
```bash
pip install -r requirements.txt
```

4. Создайте файл `.env` на основе примера:
```bash
cp .env.example .env
```
и заполните реальными значениями:
```env
YOOKASSA_ACCOUNT_ID=your_account_id
YOOKASSA_SECRET_KEY=your_secret_key
SERVER_HOST=0.0.0.0
SERVER_PORT=7270
```

5. Запустите сервер:
```bash
uvicorn main:app --reload
```

### Запуск через Docker

1. Соберите образ:
```bash
docker-compose build
```

2. Запустите контейнер:
```bash
docker-compose up
```

Сервер будет доступен по адресу: `http://localhost:7270`

## API Endpoints

### Создание платежа
`POST /create_payment/`
```json
{
  "user_id": "123",
  "price": 1000.00
}
```
Возвращает URL для оплаты, который на Frontend-части должен превращаться в QRCode

### Проверка статуса платежа
`GET /check_payment/{payment_id}`

Возвращает:
```json
{
  "status": "succeeded|pending",
  "metadata": {}  // Дополнительные данные платежа
}
```

## Переменные окружения

| Переменная              | Описание                          | Пример значения            |
|-------------------------|-----------------------------------|----------------------------|
| YOOKASSA_ACCOUNT_ID     | ID магазина в YooKassa            | 390758                     |
| YOOKASSA_SECRET_KEY     | Секретный ключ API                | test_...                   |
| SERVER_HOST             | Хост для запуска сервера          | 0.0.0.0                    |
| SERVER_PORT             | Порт для запуска сервера          | 7270                       |

## Деплой в production

1. Используйте `.env.prod` с production-ключами
2. Настройте HTTPS через Nginx
3. Для запуска рекомендуется использовать:
```bash
docker-compose -f docker-compose.prod.yml up -d
```
