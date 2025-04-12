from fastapi import FastAPI, Request
import qrcode
import yookassa
import os
from yookassa import Configuration, Payment
from payment import create
from fastapi.responses import FileResponse
import asyncio
import uvicorn
from dotenv import load_dotenv

# Загрузка переменных окружения из .env файла
load_dotenv()

app = FastAPI()

# Настройка Yookassa из переменных окружения
Configuration.account_id = os.getenv("YOOKASSA_ACCOUNT_ID")
Configuration.secret_key = os.getenv("YOOKASSA_SECRET_KEY")

def check(payment_id, user_id=None, price=None):
    payment = yookassa.Payment.find_one(payment_id)
    if payment.status == "succeeded":
        if user_id and price:
            print(f"юзер с id {user_id} оплатил на сумму {price}")
        return payment.metadata
    else:
        return False

@app.post("/create_payment/")
async def create_payment(request: Request):
    data = await request.json()
    user_id = data.get("user_id")
    price = data.get("price")  # Значение по умолчанию, если не передано
    
    # Создаем платеж
    payment_url, payment_id = create(price, user_id)
    
    # Функция для проверки статуса платежа и удаления QR-кода
    async def check_payment():
        while True:
            result = check(payment_id, user_id, price)
            if result:
                return True
            await asyncio.sleep(5)  # Проверяем каждые 5 секунд
    
    # Запускаем проверку платежа в фоне
    asyncio.create_task(check_payment())
    
    # Возвращаем QR-код клиенту
    return payment_url

@app.get("/check_payment/{payment_id}")
def check_payment_status(payment_id: str):
    result = check(payment_id)
    if result:
        return {"status": "succeeded", "metadata": result}
    return {"status": "pending"}

if __name__ == "__main__":
    host = os.getenv("SERVER_HOST", "127.0.0.1")
    port = int(os.getenv("SERVER_PORT", 7270))
    uvicorn.run(app, host=host, port=port)