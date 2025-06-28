# notify_alert.py
import requests
import os

# Tus credenciales de Ultramsg
INSTANCE_ID = os.getenv("ULTRAMSG_INSTANCE_ID", "instance128625")
TOKEN = os.getenv("ULTRAMSG_TOKEN", "wrhsqwrb45bqajz4")
TO = os.getenv("NUMERO_DESTINO", "+5491127023454")  # Con código internacional

def enviar_alerta(texto):
    url = f"https://api.ultramsg.com/{INSTANCE_ID}/messages/chat"
    payload = {
        "token": TOKEN,
        "to": TO,
        "body": texto
    }

    response = requests.post(url, data=payload)
    print(f"✅ Mensaje enviado: {response.text}")
