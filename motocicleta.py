from transporte import Transporte

class Motocicleta(Transporte):
    """Entregas pequeñas y rápidas. Máximo 100 kg y 0.5 m³."""
    
    PESO_MAX = 100.0
    VOL_MAX = 0.5

    def __init__(self, patente: str, modelo: str, costo_base_km: float = 80.0):
        super().__init__(
            patente=patente, 
            modelo=modelo, 
            peso_max=self.PESO_MAX, 
            volumen_max=self.VOL_MAX, 
            costo_base_km=costo_base_km
        )

    def calcular_impacto_ambiental(self, distancia_km: float) -> float:
        # Impacto bajo (ej: 0.05)
        return distancia_km * 0.05
    
    def calcular_costo_km(self) -> float:
        return self.costo_base_km

    def calcular_costo(self, distancia_km: float,num_pedidos: int) -> float:
        return self.costo_base_km* distancia_km
    
    def acepta_pedido_urgente(self):
        # La Motocicleta no acepta pedidos urgentes
        return False