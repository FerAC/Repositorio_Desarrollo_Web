import subprocess
import time
import pytest

def levantar_servidor(archivo_py: str, puerto: str) -> subprocess.Popen:
    comando = f"python3 {archivo_py} {puerto}"
    servidor = subprocess.Popen(comando.split())
    print(f"Servidor levantado en el puerto {puerto}")
    return servidor

def levantar_broker(archivo_py: str, puerto: str, cantidad_colas: str) -> subprocess.Popen:
    comando = f"python3 {archivo_py} {puerto} {cantidad_colas}"
    broker = subprocess.Popen(comando.split(), stdin=subprocess.PIPE)
    print(f"Broker levantado en el puerto {puerto}")
    time.sleep(10)
    return broker


def detener_servidor(servidor: subprocess.Popen) -> None:
    servidor.terminate()
    print("Servidor detenido")

def test_levantar_servidores():
    puerto = "8000"
    servidor_broker = levantar_broker("../src/message_broker.py", puerto, "2")
    servidor_productor = levantar_servidor("../src/producer.py", puerto)
    servidor_consumidor = levantar_servidor("../src/consumer.py", puerto)

    assert servidor_broker.poll() is None
    assert servidor_productor.poll() is None
    assert servidor_consumidor.poll() is None

    time.sleep(5)  # Espera 5 segundos para que los servidores se inicialicen completamente

    detener_servidor(servidor_broker)
    detener_servidor(servidor_productor)
    detener_servidor(servidor_consumidor)

if __name__ == "__main__":
    pytest.main()
