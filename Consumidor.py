import socket
import uuid
import time
from datetime import datetime
import io
from avro import schema, io as avro_io
import sys

puerto_broker_argv = sys.argv
# Configuración del consumidor
host = '127.0.0.1'  # Dirección IP del broker (localhost)
print("Puerto: " + puerto_broker_argv[1])
puerto_broker = int(puerto_broker_argv[1])  # Puerto del broker

consumidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
consumidor.connect((host, puerto_broker))
print(f"Conectado al broker en {host}:{puerto_broker} como consumidor")

# Definir el esquema Avro para la clase Message
schema_str = """
{
  "type": "record",
  "name": "Message",
  "fields": [
    {"name": "timestamp", "type": "string"},
    {"name": "id", "type": "string"},
    {"name": "header", "type": {"type": "map", "values": "string"}},
    {"name": "body", "type": {"type": "map", "values": "string"}}
  ]
}
"""

# Crear un objeto schema Avro
avro_schema = schema.Parse(schema_str)

# Función para deserializar el mensaje Avro
def deserializar_mensaje_avro(msg):
    reader = avro_io.DatumReader(avro_schema)
    bytes_reader = io.BytesIO(msg)
    decoder = avro_io.BinaryDecoder(bytes_reader)
    deserialized_msg = reader.read(decoder)
    return deserialized_msg

# Consumir mensajes
while True:
    try:
        # Notificar disponibilidad al broker
        consumidor.send(str('0').encode())
        print("Se envía status libre a Broker")

        # Esperar respuesta del broker
        msg = consumidor.recv(1024)
        if not msg:
            break

        # Empiezo a consumir
        # consumidor.send(str('1').encode())
        # print("Se envía status ocupado a Broker")

        # Deserializar el mensaje Avro
        deserialized_msg = deserializar_mensaje_avro(msg)

        print("Objeto deserializado:")
        print("Timestamp:", deserialized_msg["timestamp"])
        print("ID:", deserialized_msg["id"])
        print("Header:", deserialized_msg["header"])
        print("Body:", deserialized_msg["body"])

        time.sleep(5)
    except Exception as e:
        print("Error al deserializar:", e)

# Cerrar la conexión con el broker
consumidor.close()
