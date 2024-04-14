import time
import socket
import sys
from avro import schema, io as avro_io
from typing import List, Dict, Any

class BrokerQueue:
    """
    Clase que representa una cola de un broker.

    Attributes:
    queue_list (list): Lista que almacena las colas.
    max_sizes (list): Lista que almacena los tamaños máximos de las colas.
    queue_names (list): Lista que almacena los nombres de las colas.
    total_queues (int): Número total de colas.
    current_queue (int): Índice de la cola actual.
    current_dequeue (int): Índice de desencolado actual.
    dequeue_counter (int): Contador de desencolados.
    iterator (int): Iterador para el desencolado circular.
    """

    def __init__(self) -> None:
        """Inicializa la clase BrokerQueue."""
        self.queue_list: List[List[Any]] = []
        self.max_sizes: List[int] = []
        self.queue_names: List[str] = []
        self.total_queues: int = 0
        self.current_queue: int = 0
        self.current_dequeue: int = 0
        self.dequeue_counter: int = 0
        self.iterator: int = 0

    def find_name(self, queue_name: str) -> int:
        """
        Encuentra el índice de una cola en base a su nombre.

        Parameters:
        queue_name (str): Nombre de la cola a buscar.

        Returns:
        int: Índice de la cola en la lista de colas.

        Raises:
        ValueError: Si el nombre de la cola no se encuentra.
        """
        for i in range(self.total_queues):
            if self.queue_names[i] == queue_name:
                return i
        raise ValueError("El nombre de la cola no coincide")

    def create_queue(self, queue_name: str, max_size: int = 1000) -> None:
        """
        Crea una nueva cola en el broker.

        Parameters:
        queue_name (str): Nombre de la cola a crear.
        max_size (int): Tamaño máximo de la cola (por defecto: 1000).
        """
        my_queue: List[Any] = []
        self.queue_list.append(my_queue)
        self.max_sizes.append(max_size)
        self.queue_names.append(queue_name)
        self.total_queues += 1

    def flush_queue(self, queue_name: str, n: int = None) -> None:
        """
        Vacía una cola del broker.

        Parameters:
        queue_name (str): Nombre de la cola a vaciar.
        n (int): Número de elementos a eliminar 
        (por defecto: None, vacía la cola).

        Raises:
        ValueError: Si el nombre de la cola no se encuentra.
        """
        i: int = self.find_name(queue_name)
        if n is None:
            self.queue_list[i] = []
        else:
            del self.queue_list[i][:n]

    def delete_queue(self, queue_name: str) -> None:
        """
        Elimina una cola del broker.

        Parameters:
        queue_name (str): Nombre de la cola a eliminar.

        Raises:
        ValueError: Si el nombre de la cola no se encuentra.
        """
        i: int = self.find_name(queue_name)
        self.queue_list[i] = []
        del self.queue_list[i]
        del self.queue_names[i]
        del self.max_sizes[i]
        self.total_queues -= 1

    def is_full(self, queue_name: str) -> bool:
        """
        Verifica si una cola está llena.

        Parameters:
        queue_name (str): Nombre de la cola a verificar.

        Returns:
        bool: True si la cola está llena, False de lo contrario.

        Raises:
        ValueError: Si el nombre de la cola no se encuentra.
        """
        i: int = self.find_name(queue_name)
        return len(self.queue_list[i]) == self.max_sizes[i]

    def enqueue(self, queue_name: str, msg: Any) -> int:
        """
        Agrega un mensaje a una cola.

        Parameters:
        queue_name (str): Nombre de la cola.
        msg: Mensaje a agregar.

        Returns:
        int: 1 si el mensaje se agregó correctamente, 0 si la cola está llena.

        Raises:
        ValueError: Si el nombre de la cola no se encuentra.
        """
        i: int = self.find_name(queue_name)
        if not self.is_full(queue_name):
            self.queue_list[i].append(msg)
            if self.is_full(queue_name):
                if self.current_queue + 1 < len(self.queue_list):
                    self.current_queue += 1
                else:
                    self.current_queue = 0
            return 1
        else:
            return 0

    def is_empty(self, queue_name: str) -> bool:
        """
        Verifica si una cola está vacía.

        Parameters:
        queue_name (str): Nombre de la cola a verificar.

        Returns:
        bool: True si la cola está vacía, False de lo contrario.

        Raises:
        ValueError: Si el nombre de la cola no se encuentra.
        """
        i: int = self.find_name(queue_name)
        return len(self.queue_list[i]) == 0
    def dequeue(self, queue_name: str) -> Any:
        """
        Remueve y devuelve un mensaje de una cola.

        Parameters:
        queue_name (str): Nombre de la cola.

        Returns:
        Any: Mensaje removido de la cola, o 0 si la cola está vacía.

        Raises:
        ValueError: Si el nombre de la cola no se encuentra.
        """
        if self.is_empty(queue_name):
            return 0
        else:
            i: int = self.find_name(queue_name)
            msg: Any = self.queue_list[i].pop(0)
            empty: bool = False
            if len(self.queue_list[i]) == 0:
                self.dequeue_counter = 0
                empty = True
            else:
                self.dequeue_counter += 1

            if self.dequeue_counter >= self.max_sizes[i]:
                self.dequeue_counter = 0
                self.iterator += 1
                self.current_dequeue = self.iterator % len(self.queue_list)
            return msg

puerto_broker_argv: List[str] = sys.argv
host: str = '127.0.0.1'
puerto_broker: int = int(puerto_broker_argv[1])

cantidad_colas: int = int(puerto_broker_argv[2])
if cantidad_colas <= 0:
    aumentar_cola: str = input("La cantidad de colas debe ser un numero:"
    " mayor a 0, desea agregar un numero distinto o finalizar la "
    "ejecucion del servidor? (Y/N): ")
    if aumentar_cola == "Y":
        while cantidad_colas <= 0:
            cantidad_colas = int(input("Ingrese una cantidad valida de colas"
            " a utilizar, el numero debe ser mayor a 0: "))
    else:
        sys.exit(1)

my_queue: BrokerQueue = BrokerQueue()
for i in range(cantidad_colas):
    nombre_cola: str = f"cola_{i}"
    tamano_cola: str = input(f"Digite el tamano de la cola {i+1}: ")
    while int(tamano_cola) <= 0 or int(tamano_cola) > 1000:
        tamano_cola = input(f"Ingrese un tamano valido, debe ser mayor a 0 y"
        " menor a 1000: ")
    my_queue.create_queue(nombre_cola, int(tamano_cola))

broker: socket.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
broker.bind((host, puerto_broker))
broker.listen(1)

productor, direccion = broker.accept()

consumidor, direccion = broker.accept()
start_time: float = time.time()

primera_iteracion: bool = True
while True:
    indice_cola: int = my_queue.current_queue

    if time.time() - start_time >= 5 or primera_iteracion:
        primera_iteracion = False
        status: str = consumidor.recv(1024).decode()
    else:
        status = "1"

    if status == "0":
        start_time = time.time()
        if my_queue.is_empty(f"cola_{indice_cola}"):
            dequeue_status: Any = \
            my_queue.dequeue(f"cola_{my_queue.current_dequeue}")
            if dequeue_status == 0:
                status2: int = my_queue.enqueue(f"cola_{indice_cola}", 
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
