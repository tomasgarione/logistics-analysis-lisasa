from serviciosdeentrega import ServicioDeEntrega
from validaciones import validar_cadena_no_vacia, validar_numero_positivo
from abc import ABC, abstractmethod

class Transporte(ServicioDeEntrega, ABC):
    def __init__(self, patente: str, modelo: str, peso_max: float, volumen_max: float, costo_base_km: float):
        validar_cadena_no_vacia(patente, "Patente", "Transporte")
        validar_cadena_no_vacia(modelo, "Modelo", "Transporte")
        validar_numero_positivo(peso_max, "Peso máximo", "Transporte")
        validar_numero_positivo(volumen_max, "Volumen máximo", "Transporte")
        validar_numero_positivo(costo_base_km, "Costo base por km", "Transporte")
        self.patente = patente
        self.modelo = modelo
        self.peso_max = peso_max
        self.volumen_max = volumen_max
        self.costo_base_km = costo_base_km

    @abstractmethod
    def calcular_costo_km(self) -> float:
        pass

    def __str__(self):
        return f"Transporte(Patente: {self.patente}, Modelo: {self.modelo}, Peso Max: {self.peso_max})"