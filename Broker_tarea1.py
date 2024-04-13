import time
import socket
import sys
from avro import schema, io as avro_io


class BrokerQueue:
    def __init__(self):
        self.queue_list = []
        self.max_sizes = []
        self.queue_names = []
        self.total_queues = 0

    def find_name(self, queue_name):
        for i in range(self.total_queues):
            if self.queue_names[i] == queue_name:
                return i
        raise ValueError("El nombre de la cola no coincide")

    def create_queue(self, queue_name, max_size=1000):
        my_queue = []
        self.queue_list.insert(0, my_queue)
        self.max_sizes.insert(0, max_size)
        self.queue_names.insert(0, queue_name)
        self.total_queues += 1

    def flush_queue(self, queue_name, n=None):
        i = self.find_name(queue_name)
        if n is None:
            self.queue_list[i] = []
        else:
            del self.queue_list[i][:n]

    def delete_queue(self, queue_name):
        i = self.find_name(queue_name)
        self.queue_list[i] = []
        del self.queue_list[i]
        del self.queue_names[i]
        del self.max_sizes[i]
        self.total_queues -= 1

    def is_full(self, queue_name):
        i = self.find_name(queue_name)
        return len(self.queue_list[i]) == self.max_sizes[i]

    def enqueue(self, queue_name, msg):
        i = self.find_name(queue_name)
        if not self.is_full(queue_name):
            self.queue_list[i].append(msg)
            return 1
        else:
            a = len(self.queue_list[0])
            return 0

    def is_empty(self, queue_name):
        i = self.find_name(queue_name)
        return len(self.queue_list[i]) == 0

    def dequeue(self, queue_name):
        i = self.find_name(queue_name)
        msg = self.queue_list[i].pop(0)
        return msg

puerto_broker_argv = sys.argv
host = '127.0.0.1'  # Dirección IP del broker (localhost)
puerto_broker = int(puerto_broker_argv[1])   # Puerto del broker

my_queue = BrokerQueue()
my_queue.create_queue("cola_1", 100)

broker = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
broker.bind((host, puerto_broker))
broker.listen(1)
# print(f"Broker escuchando en {host}:{puerto_broker}")

productor, direccion = broker.accept()
# print(f"Conexión entrante del productor desde {direccion}")

consumidor, direccion = broker.accept()
# print(f"Conexión entrante del consumidor desde {direccion}")
start_time = time.time()

primera_iteracion = True
while True:
    #print("Se va a consultar disponibilidad de consumidor")
    # Consultar al consumidor si esta listo para consumir (recibir paquete de confirmacion)
    if time.time() - start_time >= 5 or primera_iteracion:
        primera_iteracion = False
        status = consumidor.recv(1024).decode()
    else:
        status = "1"

    if status == "0":
        start_time = time.time()
        #print("IIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIII\n Consumidor libre\n")
        if my_queue.is_empty("cola_1"):
            status2 = my_queue.enqueue("cola_1", productor.recv(1024))
            productor.send(str(status2).encode())
            #print("Se recibio msg de productor")
            consumidor.send(my_queue.dequeue("cola_1"))
        else:
            #print("ENTRO A ELSE\n")
            consumidor.send(my_queue.dequeue("cola_1"))
    else:
        #print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX\n Se va a encolar\n")
        status = my_queue.enqueue("cola_1", productor.recv(1024))
        productor.send(str(status).encode())
        #print("Broker recibe del productor")
    # En caso de no estarlo, sigo encolando
