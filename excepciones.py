class LisasaError(Exception):
    pass


class DatosInvalidosError(LisasaError):#Cuando alguien intenta crear algo con datos basura. 
    #Ejemplos: un artículo con peso negativo, 
    # un cliente sin nombre, un pedido sin destino.
    pass


class CapacidadExcedidaError(LisasaError): 
    #Cuando intentás meter un pedido en un viaje pero no entra en el vehículo. 
    # Ejemplo: la moto carga máximo 100 kg y querés meter un pedido de 120 kg.
    pass


class VentanaHorariaError(LisasaError):
    #Cuando intentás crear un viaje fuera de la ventana horaria permitida.
    # Ejemplo: querés crear un viaje para mañana a las 3 AM, pero solo se permiten viajes para hoy.
    pass


class EstadoPedidoError(LisasaError):
    # Cuando se intenta un cambio de estado ilegal en un pedido.
    # Ejemplo: avanzar desde ENTREGADO (estado final) no está permitido.
    # Flujo válido: PENDIENTE → EN_CAMINO → ENTREGADO.
    pass

class EstadoViajeError(LisasaError):
    # Transición de estado ilegal en un viaje.
    # Ejemplo: intentar agregar un pedido a un viaje ya EN_CURSO.
    pass