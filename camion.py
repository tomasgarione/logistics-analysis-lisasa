from transporte import Transporte

class Camion(Transporte):
    """Entregas de gran volumen. Máximo 5000 kg y 30 m³."""
    
    PESO_MAX = 5000.0
    VOL_MAX = 30.0

    def __init__(self, patente: str, modelo: str, costo_base_km: float = 200.0):
        super().__init__(
            patente=patente, 
            modelo=modelo, 
            peso_max=self.PESO_MAX, 
            volumen_max=self.VOL_MAX, 
            costo_base_km=costo_base_km
        )

    def calcular_impacto_ambiental(self, distancia_km: float) -> float:
        # Impacto alto (ej: 0.40)
        return distancia_km * 0.40

    def calcular_costo_km(self) -> float:
        # Recargo muy alto por ser un vehículo pesado ej: 150% extra
        return self.costo_base_km * 2.5
    
    def calcular_costo(self, distancia_km: float,num_pedidos: int) -> float:
        return self.calcular_costo_km() * distancia_km
    
    def acepta_pedido_urgente(self):
        # El Camión no acepta pedidos urgentes
        return False
    