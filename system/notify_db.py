# guardar_log.py
import mysql.connector
from datetime import datetime
import os

def guardar_evento(topico, mensaje, dentro_del_horario):
    conn = mysql.connector.connect(
        host=os.getenv("MYSQL_HOST", "18.230.164.213"),
        user=os.getenv("MYSQL_USER", "administrador"),
        password=os.getenv("MYSQL_PASS", "3167"),
        database=os.getenv("MYSQL_DB", "notify")
    )

    cursor = conn.cursor()

    fecha = datetime.now().strftime('%Y-%m-%d')
    hora = datetime.now().strftime('%H:%M:%S')

    query = '''
        INSERT INTO eventos (fecha, hora, topico, mensaje, fuera_de_horario)
        VALUES (%s, %s, %s, %s, %s)
    '''
    fuera_de_horario = not dentro_del_horario
    values = (fecha, hora, topico, mensaje, int(fuera_de_horario))

    cursor.execute(query, values)
    conn.commit()
    conn.close()

    print("📝 Evento registrado remotamente")
