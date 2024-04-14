import subprocess
import time

def levantar_servidor(archivo_py, puerto):
    comando = f"python3 {archivo_py} {puerto}"
    servidor = subprocess.Popen(comando.split())
    print(f"Servidor levantado en el puerto {puerto}")
    return servidor

if __name__ == "__main__":
    puerto = input("Digite el puerto a utilizar por el Broker: ")

    servidor_broker = levantar_servidor("Broker_tarea1.py", puerto)
    servidor_productor = levantar_servidor("Productor.py", puerto)
    servidor_consumidor = levantar_servidor("Consumidor.py", puerto)

    tiempo_ejecucion = input("¿Por cuánto tiempo desea mantener en "
        "línea los servidores?: ")
    try:
        print(f"Los servidores estarán activos durante"
            " {tiempo_ejecucion} segundos")
        time.sleep(int(tiempo_ejecucion))
    except KeyboardInterrupt:
        pass
    finally:
        servidor_productor.terminate()
        servidor_broker.terminate()
        servidor_consumidor.terminate()
        print("Servidores detenidos")
