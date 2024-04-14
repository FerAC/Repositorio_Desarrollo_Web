import subprocess
import time
import sys
from typing import List

def levantar_servidor(archivo_py: str, puerto: str) -> subprocess.Popen:
    """
    Función para levantar un servidor.

    Parameters:
    archivo_py (str): Nombre del archivo Python del servidor.
    puerto (str): Puerto en el que se levantará el servidor.

    Returns:
    subprocess.Popen: Proceso del servidor iniciado.
    """
    comando = f"python3 {archivo_py} {puerto}"
    servidor = subprocess.Popen(comando.split())
    print(f"Servidor levantado en el puerto {puerto}")
    return servidor

def levantar_broker(archivo_py: str, puerto: str) -> subprocess.Popen:
    """
    Función para levantar un broker.

    Parameters:
    archivo_py (str): Nombre del archivo Python del broker.
    puerto (str): Puerto en el que se levantará el broker.

    Returns:
    subprocess.Popen: Proceso del broker iniciado.
    """
    cantidad_colas: \
    str = input("Ingrese la cantidad de colas para el Broker: ")
    print("Tiene 10 segundos para configurar el broker")
    comando = f"python3 {archivo_py} {puerto} {cantidad_colas}"
    broker = subprocess.Popen(comando.split())
    print(f"Servidor levantado en el puerto {puerto}")
    time.sleep(10)
    return broker

if __name__ == "__main__":
    puerto: str = input("Digite el puerto a utilizar por el Broker: ")

    servidor_broker = levantar_broker("Broker_tarea1.py", puerto)
    servidor_productor = levantar_servidor("Productor.py", puerto)
    servidor_consumidor = levantar_servidor("Consumidor.py", puerto)

    tiempo: List[str] = sys.argv
    time.sleep(int(tiempo[1]))
    servidor_productor.terminate()
    servidor_broker.terminate()
    servidor_consumidor.terminate()
    print("Servidores detenidos")
