import random
import logging
import threading
import time

logging.basicConfig(
    format='%(asctime)s.%(msecs)03d [%(threadName)s] - %(message)s', datefmt='%H:%M:%S', level=logging.INFO)

#cantidadMaximaLatas = 10
#cantidadMaximaBotellas = 15


cantMaxHilosLectura = 3

# SI LA PETICION ES DE SOLO LECTURA SI SE PERMITE EJECUTAR MAS DE UN PROCESO
semaforoLectura = threading.Semaphore(cantMaxHilosLectura)
semaforoEscritura = threading.Semaphore(1)


class Transaccion(threading.Thread):
    def __init__(self, tipo, ejecutionTime):
        super().__init__()
        self.tipo = tipo
        self.ejecutionTime = ejecutionTime

    def ejecutarTransaccion(self):
        logging.info(
            f'Ejecutando consulta {self.tipo}')
        time.sleep(self.ejecutionTime)
        logging.info(
            f'Consulta {self.tipo} Terminada')
        if self.tipo == 'lectura':
            semaforoLectura.release()
        else:
            semaforoLectura.release()
            semaforoLectura.release()
            semaforoLectura.release()
            semaforoEscritura.release()

    def run(self):

        # PARA EJECUTAR LA PETICION EN LA BASE DE DATOS DEBO CONSULTAR SINO HAY UNA PETICION DE ESCRITURA EJECUTANDOSE
        # CONSULTO QUE NO SE ESTE EJECUTANDO OTRO HILO DE ESCRITURA

        if self.tipo == 'lectura':
            semaforoLectura.acquire()
            self.ejecutarTransaccion()

        # SI ES ESCRITURA NO DEBE ESTAR EJECUTANDOSE NINGUN PROCESO DE LECTURA POR LO QUE TOMO LOS TRES
        if self.tipo == 'escritura':
            semaforoEscritura.acquire()
            semaforoLectura.acquire()
            semaforoLectura.acquire()
            semaforoLectura.acquire()
            self.ejecutarTransaccion()


cantProcesos = random.randint(1, 20)

for i in range(cantProcesos):

    tipo = random.randint(1, 2)
    ejecutionTime = random.randint(1, 5)
    if tipo == 1:

        Transaccion('lectura', ejecutionTime).start()

    else:
        Transaccion('escritura', ejecutionTime).start()
