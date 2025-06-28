# notify_receiver.py
import RPi.GPIO as GPIO
import time
import paho.mqtt.client as mqtt
from datetime import datetime
from notify_alert import enviar_alerta
from notify_db import guardar_evento

# Configuración GPIO para sensor PIR
GPIO.setmode(GPIO.BCM)
PIR_PIN = 17  # BCM17 (pin físico 11)
GPIO.setup(PIR_PIN, GPIO.IN)

# Configuración MQTT
MQTT_BROKER = "localhost"
MQTT_PORT = 1883
MQTT_TOPIC = "notify/entrada_principal"

# Horario válido
HORARIO_DESDE = 13  # 13:00 (1 PM)
HORARIO_HASTA = 20  # 20:00 (8 PM)

# Función de detección de movimiento
def detectar_movimiento(channel):
    if GPIO.input(PIR_PIN):
        mensaje = "Movimiento detectado"
        hora_actual = datetime.now().hour
        dentro_del_horario = HORARIO_DESDE <= hora_actual < HORARIO_HASTA

        # Guardar evento en BD remota
        guardar_evento(MQTT_TOPIC, mensaje, not dentro_del_horario)
        print(f"[{datetime.now()}] Sensor PIR: {mensaje}")

        # Si está fuera de horario, enviar alerta
        if not dentro_del_horario:
            print("⚠️ ALERTA: Movimiento fuera de horario")
            enviar_alerta(
              f"*🚨 ALERTA PIR*\n❗ MOVIMIENTO DETECTADO FUERA DE HORARIO\n🕒 {datetime.now().strftime('%H:%M:%S')}"
            )

        # Publicar también por MQTT si es necesario
        client.publish(MQTT_TOPIC, mensaje)
        time.sleep(1)  # debounce

# Inicializar cliente MQTT
client = mqtt.Client()
client.connect(MQTT_BROKER, MQTT_PORT, 60)
client.loop_start()

# Configurar detection callback
GPIO.add_event_detect(PIR_PIN, GPIO.RISING, callback=detectar_movimiento)

print("⏳ Escuchando sensor PIR y broker MQTT...")

try:
    # Mantener el script corriendo
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("Detenido por usuario")
finally:
    GPIO.cleanup()
    client.loop_stop()
    client.disconnect()