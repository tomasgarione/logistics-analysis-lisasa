from excepciones import DatosInvalidosError
from transporte import Transporte

class Furgoneta(Transporte):
    """Entregas medianas. Máximo 500 kg y 10 m³."""
    
    # Constantes de clase según la documentación
    PESO_MAX = 500.0
    VOL_MAX = 10.0

    def __init__(self, patente: str, modelo: str, costo_base_km: float = 120.0):
        # Usamos super() para enviar todos los datos al constructor de Transporte.
        # Al pasarle directamente las constantes, evitamos que alguien cree
        # una furgoneta con una capacidad que no corresponde.
        super().__init__(
            patente=patente, 
            modelo=modelo, 
            peso_max=self.PESO_MAX, 
            volumen_max=self.VOL_MAX, 
            costo_base_km=costo_base_km
        )

    def calcular_impacto_ambiental(self, distancia_km: float) -> float:
        return distancia_km * 0.15  # impacto medio

    def calcular_costo_km(self) -> float:
        return self.costo_base_km * 1.3  # 30% recargo por tamaño
    
    def calcular_costo(self, distancia_km: float,num_pedidos: int) -> float:
        return self.calcular_costo_km() * distancia_km
    
    def acepta_pedido_urgente(self):
        # La Furgoneta no acepta pedidos urgentes
        return False
    