from abc import ABC, abstractmethod

class ServicioDeEntrega(ABC):

    @abstractmethod
    def calcular_costo(self, distancia_km: float, num_pedidos: int) -> float:
        pass
        
    @abstractmethod
    def calcular_impacto_ambiental(self, distancia_km: float) -> float:
        pass
        
    @abstractmethod
    def acepta_pedido_urgente(self) -> bool:
        pass
    