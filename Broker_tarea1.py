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
        self.current_queue = 0
        self.current_dequeue = 0
        self.dequeue_counter = 0
        self.iterator = 0

    def find_name(self, queue_name):
        for i in range(self.total_queues):
            if self.queue_names[i] == queue_name:
                return i
        raise ValueError("El nombre de la cola no coincide")

    def create_queue(self, queue_name, max_size=1000):
        my_queue = []
        self.queue_list.append(my_queue)
        self.max_sizes.append(max_size)
        self.queue_names.append(queue_name)
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
            print(f"Se agrega en lista {self.current_queue}")
            self.queue_list[i].append(msg)
            if self.is_full(queue_name):
                if self.current_queue + 1 < len(self.queue_list):
                    self.current_queue += 1
                else:
                    self.current_queue = 0
            return 1
        else:
            return 0

    def is_empty(self, queue_name):
        i = self.find_name(queue_name)
        return len(self.queue_list[i]) == 0

    def dequeue(self, queue_name):
        if self.is_empty(queue_name):
            return 0
        else:
            print("NOMBRE COLA:")
            print(queue_name)
            i = self.find_name(queue_name)
            print(f"Se desencola de la cola {i}, "
                "tamano maximo = {self.max_sizes[i]}")
            msg = self.queue_list[i].pop(0)
            empty = False
            if len(self.queue_list[i]) == 0:
                self.dequeue_counter = 0
                empty = True
            else:
                self.dequeue_counter += 1

            if self.dequeue_counter >= self.max_sizes[i]:
                self.dequeue_counter = 0
                self.iterator += 1
                self.current_dequeue = self.iterator % (len(self.queue_list))
            return msg


puerto_broker_argv = sys.argv
host = '127.0.0.1'
puerto_broker = int(puerto_broker_argv[1])

cantidad_colas = int(puerto_broker_argv[2])
if cantidad_colas <= 0:
    aumentar_cola = input("La cantidad de colas debe ser un numero mayor a 0,"
    " desea agregar un numero distinto o finalizar la ejecucion del servidor?"
    " (Y/N): ")
    if aumentar_cola == "Y":
        while cantidad_colas <= 0:
            cantidad_colas = int(input("Ingrese una cantidad valida de colas"
            " a utilizar, el numero debe ser mayor a 0: "))
    else:
        sys.exit(1)

my_queue = BrokerQueue()
for i in range(cantidad_colas):
    nombre_cola = f"cola_{i}"
    tamano_cola = input(f"Digite el tamano de la cola {i+1}: ")
    while int(tamano_cola) <= 0 or int(tamano_cola) > 1000:
        tamano_cola = input(f"Ingrese un tamano valido, debe ser mayor a 0 y"
        " menor a 1000: ")
    my_queue.create_queue(nombre_cola, int(tamano_cola))

broker = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
broker.bind((host, puerto_broker))
broker.listen(1)

productor, direccion = broker.accept()

consumidor, direccion = broker.accept()
start_time = time.time()

primera_iteracion = True
while True:
    indice_cola = my_queue.current_queue

    if time.time() - start_time >= 5 or primera_iteracion:
        primera_iteracion = False
        status = consumidor.recv(1024).decode()
    else:
        status = "1"

    if status == "0":
        start_time = time.time()
        if my_queue.is_empty(f"cola_{indice_cola}"):
            print("Cambio de cola")
            print(f"////SE INTENTA DE COLA {my_queue.current_dequeue} //////")
            dequeue_status = \
            my_queue.dequeue(f"cola_{my_queue.current_dequeue}")
            if dequeue_status == 0:
                print("Primera iteracion")
                status2 = my_queue.enqueue(f"cola_{indice_cola}", 
                                           productor.recv(1024))
                productor.send(str(status2).encode())
                consumidor.send(my_queue.dequeue(
                    f"cola_{my_queue.current_dequeue}"))
            else:
                consumidor.send(dequeue_status)
        else:
            consumidor.send(my_queue.dequeue(
                f"cola_{my_queue.current_dequeue}"))
    else:
        status = my_queue.enqueue(f"cola_{indice_cola}", productor.recv(1024))
        productor.send(str(status).encode())
