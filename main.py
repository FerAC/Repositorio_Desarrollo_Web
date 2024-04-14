import subprocess
import time
import sys

def levantar_servidor(archivo_py, puerto):
    comando = f"python3 {archivo_py} {puerto}"
    servidor = subprocess.Popen(comando.split())
    print(f"Servidor levantado en el puerto {puerto}")
    return servidor

def levantar_broker(archivo_py, puerto):
    cantidad_colas = input("Ingrese la cantidad de colas para el Broker: ")
    print("Tiene 10 segundos para configurar el broker")
    comando = f"python3 {archivo_py} {puerto} {cantidad_colas}"
    broker = subprocess.Popen(comando.split())
    print(f"Servidor levantado en el puerto {puerto}")
    time.sleep(10)
    return broker

if __name__ == "__main__":
    puerto = input("Digite el puerto a utilizar por el Broker: ")

    servidor_broker = levantar_broker("Broker_tarea1.py", puerto)
    servidor_productor = levantar_servidor("Productor.py", puerto)
    servidor_consumidor = levantar_servidor("Consumidor.py", puerto)

    tiempo = sys.argv
    time.sleep(int(tiempo[1]))
    servidor_productor.terminate()
    servidor_broker.terminate()
    servidor_consumidor.terminate()
    print("Servidores detenidos")
