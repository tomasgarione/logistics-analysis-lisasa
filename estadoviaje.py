from enum import Enum

class EstadoViaje(Enum):
    PLANIFICADO = "Planificado"
    EN_CURSO    = "En Curso"
    COMPLETADO  = "Completado"

    # src/estadoviaje.py
from enum import Enum

class EstadoViaje(Enum):
    PLANIFICADO = "Planificado"
    EN_CURSO    = "En Curso"
    COMPLETADO  = "Completado"

    def siguiente(self):
        if self == EstadoViaje.PLANIFICADO:
            return EstadoViaje.EN_CURSO
        if self == EstadoViaje.EN_CURSO:
            return EstadoViaje.COMPLETADO
        return None