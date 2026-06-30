from enum import Enum
from datetime import datetime
from validaciones import *
from excepciones import DatosInvalidosError 

class TipoProblema(Enum):
    DANO = "DAÑO"
    AUSENTE = "AUSENTE"
    RETRASO = "RETRASO"
    OTRO = "OTRO"

class Problema():
    def __init__(self, tipo: TipoProblema, descripcion: str, pedido_afectado = None, fecha: datetime = None):
        self.validar_tipo(tipo)
        validar_cadena_no_vacia(descripcion, "Descripción", Problema)
        if fecha is None:
            fecha = datetime.now()
        self.tipo = tipo
        self.descripcion = descripcion
        self.fecha = fecha
        self.pedido_afectado = pedido_afectado
        
    @staticmethod
    def validar_tipo(tipo):
        if not isinstance(tipo, TipoProblema):
            raise DatosInvalidosError("El tipo de problema debe ser un TipoProblema válido")
        
    def __str__ (self):
        return f"[{self.fecha}]{self.tipo.value}: {self.descripcion}"
    


        


