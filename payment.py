import yookassa
from yookassa import Payment
import uuid

def create(amount, user_id):
    id_key = str(uuid.uuid4())
    payment = Payment.create({
        "amount": {
            "value": amount,
            "currency": "RUB"
        },
        "paymnet_method_data":{
            "type" : "bank_card"
        },
        "confirmation": {
            "type": "redirect",
            "return_url": "https://t.me"
        },
        "capture": True,
        "metadata": {
          "user_id": user_id
        },
        "description": 'Пожертвование в проект'
    }, id_key)

    return payment.confirmation.confirmation_url, payment.id