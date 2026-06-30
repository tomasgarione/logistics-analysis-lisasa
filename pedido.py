from datetime import time
from estadopedido import EstadoPedido
from paquete import Paquete
from excepciones import DatosInvalidosError, EstadoPedidoError
from validaciones import *
from almacen import Almacen
from cliente import Cliente
 
 
class Pedido():
    def __init__(self, id_pedido, cliente, destino, franja_inicio, franja_fin, urgente=False):
        validar_cadena_no_vacia(id_pedido, "ID del pedido", "Pedido")
        validar_instancia(cliente, Cliente, "Cliente", "Pedido")
        validar_instancia(destino, Almacen, "Destino", "Pedido")
        validar_booleano(urgente, "Urgencia", "Pedido")
        validar_time(franja_inicio, "Franja de inicio", "Pedido")
        validar_time(franja_fin, "Franja de fin", "Pedido")
        self.validar_franja_horaria(franja_inicio, franja_fin)
        self.id_pedido = id_pedido
        self.cliente = cliente
        self.paquetes = []
        self.destino = destino
        self.franja_inicio = franja_inicio
        self.franja_fin = franja_fin
        self.incidencias = []
        self.estado = EstadoPedido.PENDIENTE
        self.urgente = urgente
        self._historial_estados: list = []
 
    def agregar_paquete(self, nuevo_paquete):
        validar_instancia(nuevo_paquete, Paquete, "Paquete", "Pedido")
        self.paquetes.append(nuevo_paquete)
 
    @staticmethod
    def validar_franja_horaria(inicio, fin):
        validar_time(inicio, "Hora de inicio", "Franja horaria")
        validar_time(fin, "Hora de fin", "Franja horaria")
        if fin <= inicio:
            raise DatosInvalidosError("La hora de fin debe ser posterior a la de inicio.")
 
    def calcular_peso_total(self):
        return sum(paquete.peso for paquete in self.paquetes)
 
    def calcular_volumen_total(self):
        return sum(paquete.volumen for paquete in self.paquetes)
 
    def agregar_incidencia(self, incidencia):
        self.incidencias.append(incidencia)
 
    def avanzar_estado(self):
        permitido = self.estado.siguiente()
        if permitido is None:
            raise EstadoPedidoError(
                f"El pedido '{self.id_pedido}' ya está en estado final."
            )
        self._historial_estados.append(self.estado)
        self.estado = permitido
 
    def revertir_estado(self):
        if not self._historial_estados:
            raise EstadoPedidoError(
                f"El pedido '{self.id_pedido}' no tiene estados anteriores para revertir."
            )
        self.estado = self._historial_estados.pop()
 
    def obtener_historial_estados(self):
        return list(self._historial_estados)
 
    def __str__(self):
        return (
            f"Pedido(ID: {self.id_pedido}, Cliente: {self.cliente}, "
            f"Destino: {self.destino}, Estado: {self.estado.value})"
        )