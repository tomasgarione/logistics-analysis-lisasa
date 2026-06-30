from datetime import time
from validaciones import *
from excepciones import CapacidadExcedidaError, VentanaHorariaError,DatosInvalidosError
from estadoviaje import EstadoViaje
from excepciones import EstadoViajeError
from almacen import Almacen
from ruta import Ruta
from serviciosdeentrega import ServicioDeEntrega

class Viaje:
    
    COSTO_FIJO_POR_PARADA = 500.0
    
    def __init__(self, id_viaje, transporte, almacen_origen, ruta, hora_salida: time):
        validar_cadena_no_vacia(id_viaje, "ID del viaje", "Viaje")
        self.validar_objetos(transporte, almacen_origen, ruta)
        self.id_viaje = id_viaje
        self.transporte = transporte  # Objeto (Moto, Furgoneta o Camion)
        self.almacen_origen = almacen_origen  # Objeto Almacen
        self.ruta = ruta  # Objeto Ruta
        self.hora_salida = hora_salida
        self.pedidos = []  # Lista de pedidos aceptados
        self.estado = EstadoViaje.PLANIFICADO

    def agregar_pedido(self, nuevo_pedido):
        if self.estado != EstadoViaje.PLANIFICADO:
            raise EstadoViajeError("Solo se pueden agregar pedidos a viajes en estado PLANIFICADO.")
        
        if nuevo_pedido.urgente and not self.transporte.acepta_pedido_urgente():
            raise DatosInvalidosError("Un pedido urgente solo puede asignarse a un Mensajero Externo.")
        if not nuevo_pedido.urgente and self.transporte.acepta_pedido_urgente():
            raise DatosInvalidosError("Un Mensajero Externo solo transporta pedidos urgentes.")

        if not self.ruta.incluye_almacen(nuevo_pedido.destino):
            raise DatosInvalidosError("La ruta del viaje no incluye el almacén destino del pedido.")
        
        # 1. VALIDACIÓN TEMPORAL (Le pregunta a la Ruta)
        if not self.ruta.verificar_ventana(nuevo_pedido, self.hora_salida):
            raise VentanaHorariaError(f"El pedido {nuevo_pedido.id_pedido} no llega a tiempo.")

        # 2. VALIDACIÓN FÍSICA (Suma lo que ya tiene + el nuevo)
        peso_total_actual = sum(p.calcular_peso_total() for p in self.pedidos)
        volumen_total_actual = sum(p.calcular_volumen_total() for p in self.pedidos)

        nuevo_peso = peso_total_actual + nuevo_pedido.calcular_peso_total()
        nuevo_volumen = volumen_total_actual + nuevo_pedido.calcular_volumen_total()

        if nuevo_peso > self.transporte.peso_max:
            raise CapacidadExcedidaError("Se supera el peso máximo del transporte.")
        
        if nuevo_volumen > self.transporte.volumen_max:
            raise CapacidadExcedidaError("Se supera el volumen máximo del transporte.")

        # 3. SI TODO ESTÁ OK: Se registra el pedido
        self.pedidos.append(nuevo_pedido)
    
    def iniciar(self):
        if self.estado != EstadoViaje.PLANIFICADO:
            raise EstadoViajeError(
                f"Solo se puede iniciar un viaje PLANIFICADO. Estado actual: {self.estado.value}"
            )
        self.estado = EstadoViaje.EN_CURSO

    def completar(self):
        if self.estado != EstadoViaje.EN_CURSO:
            raise EstadoViajeError(
                f"Solo se puede completar un viaje EN_CURSO. Estado actual: {self.estado.value}"
            )
        self.estado = EstadoViaje.COMPLETADO

    def obtener_costo_total(self):
        
        distancia=self.ruta.calcular_distancia_total()
        cantidad_pedidos=len(self.pedidos)

        # Creamos un conjunto con los almacenes de destino de los pedidos y vemos cuántos son para calcular las paradas (si hay varios pedidos al mismo destino, solo cuenta como una parada)
        cantidad_paradas = len(set(pedido.destino for pedido in self.pedidos))
        return self.transporte.calcular_costo(distancia,cantidad_pedidos) + cantidad_paradas * self.COSTO_FIJO_POR_PARADA

    def obtener_impacto_ambiental(self):
        # Distancia * Emisiones de CO2 del vehículo
        distancia = self.ruta.calcular_distancia_total()
        return self.transporte.calcular_impacto_ambiental(distancia) 


    @staticmethod
    def validar_objetos(transporte, almacen, ruta):
        validar_instancia(transporte, ServicioDeEntrega, "Servicio de Entrega", "Viaje")
        validar_instancia(almacen, Almacen, "Almacén", "Viaje")
        validar_instancia(ruta, Ruta, "Ruta", "Viaje")