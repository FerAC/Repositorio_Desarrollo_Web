# Sistema de mensajería

En esta implementacion se desarrolla un sistema de mensajería básico en python.
El sistema consta de tres partes:

-**Productor**: Se encarga de producir mensajes que posteriormente seran enviados al broker para que sean encolados.

-**Broker**: Encargado de la comunicación entre el productor y el consumidor, también posee un sistema de colas donde almacena los mensajes enviados por el productor para que posteriormente sean enviados al consumidor.

-**Consumidor**: Consume los mensajes enviados por el productor, deserializa e imprime los mensajes.

En adicion se incluye un script "main.py" que puede levantar los tres servidores por si mismo por un tiempo determinado.

## Requisitos

Para el correcto funcionamiento del sistema es necesario ejecutarlo en un sistema Unix. Para el desarrollo del mismo fue utilizado Ubuntu 20.04 LTS.

Tener instalado Python 3.8.10

No se asegura el correcto funcionamiento del sistema si no se cumple con estos requisitos

## Intrucciones de Uso

### Mediante "main.py"

1. Abrir una terminal Unix en la carpeta src del repositorio.
2. Escribir el siguiente comando, donde tiempo en segundos corresponde a la cantidad del segundos que el servidor estara en linea:

```bash
python3 main.py tiempo_ejecucion_en_segundos 
```

Una consideracion importante a tener en cuenta es que una vez que se empiece a configurar el broker el usuario dispone de 10 segundos para la configuracion de las colas, posterior a este tiempo el sistema se levantará.

### Individualmente

Si se desea tambien es posible levantar el sistema utilizando cada servicio por separado. El orden en el que se realizan los pasos es de vital importancia para el correcto funcionamiento del sistema.

1. Abrir una terminal Unix en la carpeta src del repositorio.
2. Escribir el siguiente comando, donde puerto representa al puerto donde debe correr el broker, y cantidad_colas es el numero de colas del broker:

```bash
python3 message_broker.py puerto cantidad_colas
```

3. Digitar el tamaño de las n colas requeridas.
4. Abrir otra terminal Unix en la carpeta src del repositorio.
5. Escribir el siguiente comando, donde puerto representa al puerto donde se inició el broker:

```bash
python3 producer.py puerto
```

6. Abrir otra terminal Unix en la carpeta src del repositorio.
5. Escribir el siguiente comando, donde puerto representa al puerto donde se inició el broker:

```bash
python3 consumer.py puerto
```

Para finalizar la ejecución del sistema ingrese las teclas <kbd>Ctrl</kbd> + <kbd>C</kbd> en la terminal donde este corriendo el broker.

## Outputs

Con el objetivo de monitorear y llevar bitácora del correcto funcionamiento del sistema, en cada ejecución del sistema se generan dos outputs, uno del consumidor y otro del productor.

### Consumidor

El output del consumidor muestra los mensajes consumidos de manera efectiva por el consumidor, esto lo hace guardando los datos deseralizados.

### Productor

Muestra el numero del mensaje enviado, y un estado del envío, 0 para envío fallido (no se pudo encolar) y 1 para envío exitoso.