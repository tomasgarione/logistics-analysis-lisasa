from transporte import ServicioDeEntrega
from validaciones import validar_cadena_no_vacia

class MensajeroExterno(ServicioDeEntrega):
    TARIFA_FIJA_POR_SOLICITUD = 1500.0
    PESO_MAX = 2000.0
    VOL_MAX = 12.0
    
    def __init__(self, patente: str, modelo: str):
        validar_cadena_no_vacia(patente, "Patente", "MensajeroExterno")
        validar_cadena_no_vacia(modelo, "Modelo", "MensajeroExterno")
        self.patente = patente
        self.modelo = modelo
        self.peso_max = MensajeroExterno.PESO_MAX
        self.volumen_max = MensajeroExterno.VOL_MAX

    def calcular_impacto_ambiental(self, distancia_km: float) -> float:
        return 0.0

    def calcular_costo(self, distancia_km: float, num_pedidos: int) -> float:
        return self.TARIFA_FIJA_POR_SOLICITUD * num_pedidos
    
    def acepta_pedido_urgente(self) -> bool:
        return True

    def __str__(self):
        return f"MensajeroExterno(Proveedor: {self.modelo}, Patente: {self.patente})"
