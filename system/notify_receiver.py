# notify_receiver_ir.py
import RPi.GPIO as GPIO
import time
import paho.mqtt.client as mqtt
from datetime import datetime
from notify_alert import enviar_alerta
from notify_db import guardar_evento

# Configuración GPIO para sensor IR
GPIO.setmode(GPIO.BCM)
IR_PIN = 17  # BCM17 (pin físico 11) - Pin de salida del sensor IR
GPIO.setup(IR_PIN, GPIO.IN)

# Configuración MQTT
MQTT_BROKER = "localhost"
MQTT_PORT = 1883
MQTT_TOPIC = "notify/entrada_principal"

# Horario válido
HORARIO_DESDE = 13  # 13:00 (1 PM)
HORARIO_HASTA = 20  # 20:00 (8 PM)

# Función de detección de interrupción del haz IR
def detectar_interrupcion(channel):
    # La lógica para el sensor IR puede variar. Algunos sensores detectan interrupción
    # con un estado "HIGH" (1) y otros con un estado "LOW" (0). 
    # Asegúrate de verificar cuál es el caso de tu sensor específico.
    # El código actual asume que detecta interrupción con un estado HIGH, igual que el PIR.
    if GPIO.input(IR_PIN):
        mensaje = "Haz IR interrumpido"
        hora_actual = datetime.now().hour
        dentro_del_horario = HORARIO_DESDE <= hora_actual < HORARIO_HASTA

        # Guardar evento en BD remota
        guardar_evento(MQTT_TOPIC, mensaje, not dentro_del_horario)
        print(f"[{datetime.now()}] Sensor IR: {mensaje}")

        # Si está fuera de horario, enviar alerta
        if not dentro_del_horario:
            print("⚠️ ALERTA: Interrupción de haz IR fuera de horario")
            enviar_alerta(
              f"*🚨 ALERTA IR*\n❗ HAZ INTERRUMPIDO FUERA DE HORARIO\n🕒 {datetime.now().strftime('%H:%M:%S')}"
            )

        # Publicar también por MQTT si es necesario
        client.publish(MQTT_TOPIC, mensaje)
        time.sleep(1)  # debounce

# Inicializar cliente MQTT
client = mqtt.Client()
client.connect(MQTT_BROKER, MQTT_PORT, 60)
client.loop_start()

# Configurar detection callback
# Aquí usamos GPIO.RISING, asumiendo que la interrupción del haz
# hace que la salida del sensor IR pase de LOW a HIGH.
# Si tu sensor funciona al revés, cambia GPIO.RISING por GPIO.FALLING.
GPIO.add_event_detect(IR_PIN, GPIO.RISING, callback=detectar_interrupcion)

print("⏳ Escuchando sensor IR y broker MQTT...")

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
