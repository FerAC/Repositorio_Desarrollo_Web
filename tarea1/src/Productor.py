import uuid
from datetime import datetime
import io
from avro import schema, io as avro_io
import socket
import sys

# Configuración del cliente
puerto_broker_argv = sys.argv
host = '127.0.0.1'  # Dirección IP del servidor (localhost)
puerto_broker = int(puerto_broker_argv[1])   # Puerto de conexión

productor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
productor.connect((host, puerto_broker))

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

# Definir la clase Message
class Message:
    def __init__(self, header, body):
        self.timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.id = str(uuid.uuid4())
        self.header = header
        self.body = body

# Abre un archivo en modo escritura
i = 0
with open('../output/outputProductor.txt', 'w') as archivo:
    while True:
        # Crear una instancia de la clase Message
        msg = Message({"header": "reunion NUMERO: " + str(i)}, {"body": 
          "la reunion es hoy"})

        # Serializar el objeto Message utilizando Avro
        writer = avro_io.DatumWriter(avro_schema)
        bytes_writer = io.BytesIO()
        encoder = avro_io.BinaryEncoder(bytes_writer)
        writer.write({"timestamp": msg.timestamp, "id": msg.id, "header": 
          msg.header, "body": msg.body}, encoder)

        # Obtener los bytes serializados
        serialized_data = bytes_writer.getvalue()

        productor.send(serialized_data)
        status = productor.recv(1024).decode()
        archivo.write(f"Estado de encolado: {status}"
          f" En el paquete numero: {i}\n")
        i += 1
