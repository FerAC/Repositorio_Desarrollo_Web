import uuid
from datetime import datetime
import io
from avro import schema, io as avro_io
import socket
import sys
from typing import Dict, Any, List

# Configuración del cliente
puerto_broker_argv: List[str] = sys.argv
host: str = '127.0.0.1'  # Dirección IP del servidor (localhost)
puerto_broker: int = int(puerto_broker_argv[1])  # Puerto de conexión

productor: socket.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
productor.connect((host, puerto_broker))

# Definir el esquema Avro para la clase Message
schema_str: str = """
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
avro_schema: schema.Schema = schema.Parse(schema_str)

# Definir la clase Message
class Message:
    def __init__(self, header: Dict[str, str], body: Dict[str, str]):
        self.timestamp: str = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.id: str = str(uuid.uuid4())
        self.header: Dict[str, str] = header
        self.body: Dict[str, str] = body

# Abre un archivo en modo escritura
i: int = 0
with open('../output/outputProductor.txt', 'w') as archivo:
    while True:
        # Crear una instancia de la clase Message
        msg: Message = Message({"header": "reunion NUMERO: " + str(i)},\
          {"body": "la reunion es hoy"})

        # Serializar el objeto Message utilizando Avro
        writer: avro_io.DatumWriter = avro_io.DatumWriter(avro_schema)
        bytes_writer: io.BytesIO = io.BytesIO()
        encoder: avro_io.BinaryEncoder = avro_io.BinaryEncoder(bytes_writer)
        writer.write({"timestamp": msg.timestamp, "id": msg.id, "header": msg.header,\
         "body": msg.body}, encoder)

        # Obtener los bytes serializados
        serialized_data: bytes = bytes_writer.getvalue()

        productor.send(serialized_data)
        status: str = productor.recv(1024).decode()
        archivo.write(f"Estado de encolado: {status} En el paquete numero: {i}\n")
        i += 1
# Cerrar la conexión con el broker
productor.close()