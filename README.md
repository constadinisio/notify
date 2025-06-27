# NOTIFY

### 🧩 ¿Qué es Notify?

**Notify** es un sistema de **seguridad inteligente basado en IoT**, que utiliza un **sensor de movimiento** para detectar actividad fuera del horario normal y enviar alertas instantáneas al celular mediante **Telegram o WhatsApp**.

---

### 🎯 Objetivo del proyecto

Detectar movimientos **no autorizados** en entornos que deberían estar vacíos (ej: oficinas por la noche, depósitos, aulas cerradas) y **notificar al instante al usuario** para actuar rápidamente ante posibles intrusiones.

---

### ⚙️ ¿Cómo funciona?

1. Un **sensor de movimiento PIR** está conectado a un dispositivo IoT (ESP32, Raspberry, etc.).
2. El sistema se activa automáticamente fuera del horario habitual.
3. Ante cualquier movimiento detectado, el sensor envía una **alerta al broker MQTT**.
4. Un **servidor MQTT listener** procesa esa alerta y **la reenvía como mensaje** a través de **Telegram o WhatsApp**.
5. El usuario recibe la notificación en tiempo real.

---

### 📲 ¿Qué recibe el usuario?

Una alerta como:

> 🚨 Alerta de movimiento detectado
> 
> 
> Hora: 03:17
> 
> Ubicación: Aula 2 – Planta Baja
> 

(Con posibilidad de incluir ubicación, imágenes o video en versiones avanzadas)

---

### 🛡️ Ventajas de Notify

- ✅ Notificaciones en tiempo real
- ✅ Bajo costo de hardware
- ✅ Sincronizable con horarios definidos
- ✅ Funciona por Wi-Fi
- ✅ Escalable a múltiples sensores o zonas

---

### 🔒 Aplicaciones posibles

- Seguridad nocturna en oficinas, aulas, o galpones
- Control de movimiento en zonas restringidas
- Monitoreo inteligente sin intervención humana
