# notify_receiver_sim_button.py
import RPi.GPIO as GPIO
import time
import paho.mqtt.client as mqtt
from datetime import datetime
from notify_alert import enviar_alerta
from notify_db import guardar_evento

# Configuración GPIO para el botón
GPIO.setmode(GPIO.BCM)
BUTTON_PIN = 17  # BCM17 (pin físico 11)
# Configura el pin como entrada con resistencia pull-up interna
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Configuración MQTT
MQTT_BROKER = "localhost"
MQTT_PORT = 1883
MQTT_TOPIC = "notify/entrada_principal"

# Horario válido
HORARIO_DESDE = 13  # 13:00 (1 PM)
HORARIO_HASTA = 20  # 20:00 (8 PM)

# Función de detección de pulsación del botón
def detectar_pulsacion(channel):
    # Cuando el botón es presionado, el pin cambia de HIGH a LOW.
    # Por eso usamos GPIO.FALLING.
    if GPIO.input(BUTTON_PIN) == GPIO.LOW:
        mensaje = "Botón presionado (simulación IR)"
        hora_actual = datetime.now().hour
        dentro_del_horario = HORARIO_DESDE <= hora_actual < HORARIO_HASTA

        # Guardar evento en BD remota
        guardar_evento(MQTT_TOPIC, mensaje, not dentro_del_horario)
        print(f"[{datetime.now()}] Simulación: {mensaje}")

        # Si está fuera de horario, enviar alerta
        if not dentro_del_horario:
            print("⚠️ ALERTA: Evento de simulación fuera de horario")
            enviar_alerta(
              f"*🚨 ALERTA SIMULACIÓN*\n❗ BOTÓN PRESIONADO FUERA DE HORARIO\n🕒 {datetime.now().strftime('%H:%M:%S')}"
            )

        # Publicar también por MQTT
        client.publish(MQTT_TOPIC, mensaje)

# Inicializar cliente MQTT
client = mqtt.Client()
client.connect(MQTT_BROKER, MQTT_PORT, 60)
client.loop_start()

# Configurar detection callback para el flanco de bajada
GPIO.add_event_detect(BUTTON_PIN, GPIO.FALLING, callback=detectar_pulsacion, bouncetime=200)

print("⏳ Presiona el botón para simular una detección...")

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
