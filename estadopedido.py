from enum import Enum

class EstadoPedido(Enum):
    PENDIENTE = "Pendiente"
    EN_CAMINO = "En Camino"
    ENTREGADO = "Entregado"

    def siguiente(self):
        if self == EstadoPedido.PENDIENTE:
            return EstadoPedido.EN_CAMINO
        elif self == EstadoPedido.EN_CAMINO:
            return EstadoPedido.ENTREGADO
        else:
            return None  # No hay siguiente estado para ENTREGADO
# Define las transiciones permitidas entre estados de pedido evitando el uso excesivo de ifs.
