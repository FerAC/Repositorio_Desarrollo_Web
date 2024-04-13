import subprocess
import time

# Función para levantar un servidor en un archivo .py específico y puerto determinado
def levantar_servidor(archivo_py, puerto):
    comando = f"python3 {archivo_py} {puerto}"
    servidor = subprocess.Popen(comando.split())
    print(f"Servidor levantado en el puerto " + puerto)
    return servidor

if __name__ == "__main__":
    puerto = input("Digite el puerto a utilizar por el Broker: ")
    
    # Levantar los servidores en procesos separados
    servidor_broker = levantar_servidor("Broker_tarea1.py", puerto)
    servidor_productor = levantar_servidor("Productor.py", puerto)
    servidor_consumidor = levantar_servidor("Consumidor.py", puerto)

    tiempo_ejecucion = input("¿Por cuanto tiempo desea mantener en linea los servidores?: ")
    try:
        # Mantener los servidores levantados durante un tiempo determinado
        
        print(f"Los servidores estarán activos durante {tiempo_ejecucion} segundos")
        time.sleep(tiempo_ejecucion)
    except KeyboardInterrupt:
        # Capturar la interrupción del teclado (Ctrl+C) para detener los servidores
        pass
    finally:
        # Detener los servidores al finalizar
        servidor_productor.terminate()
        servidor_broker.terminate()
        servidor_consumidor.terminate()
        print("Servidores detenidos")
