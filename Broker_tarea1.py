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
        self.currrent_queue = 0
        self.currrent_dequeue = 0
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
            print(f"Se agrega en lista {self.currrent_queue}")
            self.queue_list[i].append(msg)
            #Verifico si anadir ese elemento lleno la cola
            if self.is_full(queue_name):
                #Aumento el indice de cola actual si hay mas colas disponibles
                if self.currrent_queue+1 < len(self.queue_list):
                    self.currrent_queue+=1
                else:
                    self.currrent_queue = 0
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
            print("NOMBRE COLA: ")
            print(queue_name)
            i = self.find_name(queue_name)
            print(f"Se desencola de la cola {i}, tamano maximo = {self.max_sizes[i]}")
            msg = self.queue_list[i].pop(0)
            vacia = False
            if len(self.queue_list[i]) == 0:
                self.dequeue_counter = 0
                vacia = True
            else:
                self.dequeue_counter+=1

            if self.dequeue_counter >= self.max_sizes[i]:
                self.dequeue_counter = 0
                my_queue.iterator +=1
                self.currrent_dequeue = self.iterator % (len(self.queue_list))
                print(f"Termine con cola, proxima cola: {self.currrent_dequeue}")

            # #Verifico si ya desencole todos los elementos de una cola
            # if self.dequeue_counter > self.max_sizes[i] or vacia: 
            #     #Si estoy en la primera cola, revisar que la siguiente 
            #     if self.currrent_dequeue == 0 and len(self.queue_list) > 1:
            #         if len(self.queue_list[1])>0:
            #             self.currrent_dequeue = 1
            #     else:
            #         self.currrent_dequeue = self.currrent_dequeue % len(self.queue_list)
            return msg


        

puerto_broker_argv = sys.argv
host = '127.0.0.1'  # Dirección IP del broker (localhost)
puerto_broker = int(puerto_broker_argv[1])   # Puerto del broker

cantidad_colas = int(puerto_broker_argv[2])
if(cantidad_colas<=0):
    aumentar_cola = input("La cantidad de colas debe ser un numero mayor a 0, desea agregar un numero distinto o finalizar la ejecucion del servidor? (Y/N): ")
    if aumentar_cola == "Y":
        while cantidad_colas <= 0:
            cantidad_colas = int(input("Ingrese una cantidad valida de colas a utilizar, el numero debe ser mayor a 0: "))
    else:
        sys.exit(1)

my_queue = BrokerQueue()
for i in range(cantidad_colas):
    nombre_cola = f"cola_{i}"
    tamano_cola = input(f"Digite el tamano de la cola {i+1}: ")
    while(int(tamano_cola)<=0 or int(tamano_cola)>1000):
        tamano_cola = input(f"Ingrese un tamano valido, debe ser mayor a 0 y menor a 1000: ")
    my_queue.create_queue(nombre_cola, int(tamano_cola))


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
    
    indice_cola = my_queue.currrent_queue
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
        if my_queue.is_empty(f"cola_{indice_cola}"):
            print("Cambio de cola")
            #Intenta desencolar, si no puede encola
            print(f"////SE INTENTA DE COLA {my_queue.currrent_dequeue} ///////")
            dequeue_status = my_queue.dequeue(f"cola_{my_queue.currrent_dequeue}")
            if dequeue_status == 0:
                print("Primera iteracion")
                status2 = my_queue.enqueue(f"cola_{indice_cola}", productor.recv(1024))
                productor.send(str(status2).encode())
                #print("Se recibio msg de productor")
                consumidor.send(my_queue.dequeue(f"cola_{my_queue.currrent_dequeue}"))
            else:
                consumidor.send(dequeue_status)
        else:
            #print("ENTRO A ELSE\n")
            consumidor.send(my_queue.dequeue(f"cola_{my_queue.currrent_dequeue}"))
    else:
        #print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX\n Se va a encolar\n")
        status = my_queue.enqueue(f"cola_{indice_cola}", productor.recv(1024))
        productor.send(str(status).encode())
        #print("Broker recibe del productor")
    
    # En caso de no estarlo, sigo encolando
