import random
import logging
import threading
import time

from Cola import Cola

logging.basicConfig(
    format='%(asctime)s.%(msecs)03d [%(threadName)s] - %(message)s', datefmt='%H:%M:%S', level=logging.INFO)

#cantidadMaximaLatas = 10
#cantidadMaximaBotellas = 15
colaLecturaClientes = Cola()
colaEscrituraClientes = Cola()
colaLecturaProductos = Cola()
colaEscrituraProductos = Cola()

cantMaxHilosLectura = 3

# SI LA PETICION ES DE SOLO LECTURA SI SE PERMITE EJECUTAR MAS DE UN PROCESO
semaforoProducto = threading.Semaphore(cantMaxHilosLectura)
semaforoEscrituraProducto = threading.Semaphore(1)
semaforoCliente = threading.Semaphore(cantMaxHilosLectura)
semaforoEscrituraCliente = threading.Semaphore(1)


class GestorDeTransacciones(threading.Thread):
    def __init__(self, transaccion):
        super().__init__()
        self.transaccion = transaccion

    def encolarPeticionLectura(self):
        if self.transaccion.tabla == 'clientes':
            # ENCOLO LA TRANSACCION DE LA TABLA CLIENTE EN LA COLA DE CLIENTES LECTURA
            colaLecturaClientes.encolar(self.transaccion)
        elif self.transaccion.tabla == 'productos':
            # ENCOLO LA TRANSACCION DE LA TABLA PRODUCTOS EN LA COLA DE PRODUCTOS LECTURA
            colaLecturaProductos.encolar(self.transaccion)

    def encolarPeticionEscritura(self):
        if self.transaccion.tabla == 'clientes':
            # ENCOLO LA TRANSACCION DE LA TABLA CLIENTE EN LA COLA DE CLIENTES LECTURA
            colaEscrituraClientes.encolar(self.transaccion)
        elif self.transaccion.tabla == 'productos':
            # ENCOLO LA TRANSACCION DE LA TABLA PRODUCTOS EN LA COLA DE PRODUCTOS LECTURA
            colaEscrituraProductos.encolar(self.transaccion)

    def run(self):
        if self.transaccion.tipo == 'lectura':
            self.encolarPeticionLectura()
        elif self.transaccion.tipo == 'escritura':
            self.encolarPeticionEscritura()


class Transaccion(threading.Thread):
    def __init__(self, tipo, ejecutionTime, tabla):
        super().__init__()
        self.tipo = tipo
        self.ejecutionTime = ejecutionTime
        # SE INDICA LA TABLA PARA SABER SOBRE CUAL SE REALIZA LA CONSULTA
        self.tabla = tabla

    def ejecutarTransaccion(self):
        logging.info(
            f'Ejecutando consulta {self.tipo} en la tabla {self.tabla}')
        time.sleep(self.ejecutionTime)
        logging.info(
            f'Consulta {self.tipo} en la tabla {self.tabla} Terminada')
        if self.tipo == 'lectura':
            if self.tabla == 'cliente':
                semaforoCliente.release()
            else:
                semaforoProducto.release()
        else:
            if self.tabla == 'cliente':
                semaforoCliente.release()
                semaforoCliente.release()
                semaforoCliente.release()
                semaforoEscrituraCliente.release()
            else:
                semaforoProducto.release()
                semaforoProducto.release()
                semaforoProducto.release()
                semaforoEscrituraProducto.release()

    def run(self):

        # PARA EJECUTAR LA PETICION EN LA BASE DE DATOS DEBO CONSULTAR SINO HAY UNA PETICION DE ESCRITURA EJECUTANDOSE
        # CONSULTO QUE NO SE ESTE EJECUTANDO OTRO HILO DE ESCRITURA

        if self.tipo == 'lectura':

            self.ejecutarTransaccion()

        # SI ES ESCRITURA NO DEBE ESTAR EJECUTANDOSE NINGUN PROCESO DE LECTURA POR LO QUE TOMO LOS TRES
        if self.tipo == 'escritura':
            self.ejecutarTransaccion()


# RECORRO CONSTANTEMENTE LAS COLAS PARA EJECUTARLAS
# COLA DE LECTURA CLIENTES
class ControlLecturaCliente(threading.Thread):
    def __init__(self):
        super().__init__()

    def run(self):
        while(True):
            # LA COLA DE CLIENTES LECTURA ES MAYOR QUE 0?
            if not colaLecturaClientes.estaVacia():
                semaforoCliente.acquire()
                # HAGO UN POP DE LA COLA DE CLIENTES Y EJECUTO LA TRANSACCION
                colaLecturaClientes.desencolar().start()

# COLA DE LECTURA CLIENTES


class ControlEscrituraCliente(threading.Thread):
    def __init__(self):
        super().__init__()

    def run(self):
        # COLA DE ESCRITURA CLIENTES
        while(True):
            # LA COLA DE CLIENTES ESCRITURA ES MAYOR QUE 0?
            if not colaEscrituraClientes.estaVacia():
                semaforoEscrituraCliente.acquire()
                semaforoCliente.acquire()
                semaforoCliente.acquire()
                semaforoCliente.acquire()
                # HAGO UN POP DE LA COLA DE CLIENTES Y EJECUTO LA TRANSACCION
                colaEscrituraClientes.desencolar().start()


class ControlLecturaProductos(threading.Thread):
    def __init__(self):
        super().__init__()

    def run(self):
        # COLA DE LECTURA PRODUCTOS
        while(True):
            # LA COLA DE PRODUCTOS LECTURA ES MAYOR QUE 0?
            if not colaLecturaProductos.estaVacia():
                semaforoProducto.acquire()
                # HAGO UN POP DE LA COLA DE PRODUCTOS LECTURA Y EJECUTO LA TRANSACCION
                colaLecturaProductos.desencolar().start()


class ControlEscrituraProductos(threading.Thread):
    def __init__(self):
        super().__init__()

    def run(self):
        # COLA DE ESCRITURA PRODUCTOS
        while(True):
            # LA COLA DE PRODUCTOS ESCRITURA ES MAYOR QUE 0?
            if not colaEscrituraProductos.estaVacia():
                semaforoEscrituraProducto.acquire()
                semaforoProducto.acquire()
                semaforoProducto.acquire()
                semaforoProducto.acquire()
                # HAGO UN POP DE LA COLA DE PRODUCTOS ESCRITURA Y EJECUTO LA TRANSACCION
                colaEscrituraProductos.desencolar().start()


ControlLecturaCliente().start()
ControlEscrituraCliente().start()
ControlLecturaProductos().start()
ControlEscrituraProductos().start()

cantProcesos = random.randint(5, 20)

for i in range(cantProcesos):

    tipo = random.randint(1, 2)
    ejecutionTime = random.randint(1, 5)
    tabla = random.randint(1, 2)
    if tipo == 1:

        if tipo == 1:
            GestorDeTransacciones(Transaccion(
                'lectura', ejecutionTime, 'clientes')).start()
        else:
            GestorDeTransacciones(Transaccion(
                'lectura', ejecutionTime, 'productos')).start()

    else:
        if tipo == 1:
            GestorDeTransacciones(Transaccion(
                'escritura', ejecutionTime, 'clientes')).start()
        else:
            GestorDeTransacciones(Transaccion(
                'escritura', ejecutionTime, 'productos')).start()
