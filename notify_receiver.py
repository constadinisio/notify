# notify_receiver.py
import paho.mqtt.client as mqtt
from datetime import datetime
from notify_alert import enviar_alerta

# Configuración
MQTT_BROKER = "localhost"
MQTT_PORT = 1883
MQTT_TOPIC = "notify/#"

HORARIO_DESDE = 8    # 08:00 AM
HORARIO_HASTA = 20   # 08:00 PM

# Función al recibir mensaje

def on_connect(client, userdata, flags, rc):
    print("✅ Conectado al broker MQTT con código:", rc)
    client.subscribe(MQTT_TOPIC)

def on_message(client, userdata, msg):
    hora_actual = datetime.now().hour
    dentro_del_horario = HORARIO_DESDE <= hora_actual < HORARIO_HASTA
    mensaje = msg.payload.decode()

    print(f"[{datetime.now()}] Mensaje recibido en {msg.topic}: {mensaje}")

    if not dentro_del_horario:
        print("⚠️ ALERTA: Movimiento fuera de horario")
        enviar_alerta(f"*🚨 ALERTA*\n❗ MOVIMIENTO DETECTADO FUERA DE HORARIO\n🕒 {datetime.now().strftime('%H:%M:%S')}")

# Conexión al broker
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(MQTT_BROKER, MQTT_PORT, 60)
print("⏳ Escuchando eventos de movimiento...")
client.loop_forever()