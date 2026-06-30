from datetime import datetime, time
from excepciones import DatosInvalidosError
from typing import Union
 
 
def validar_numero_positivo(num: Union[int, float], nombre_campo: str = "", nombre_clase: str = ""):
    if not isinstance(num, (int, float)) or num <= 0:
        sujeto = f"{nombre_campo} " if nombre_campo else "El valor "
        contexto = f"de {nombre_clase} " if nombre_clase else ""
        raise DatosInvalidosError(f"{sujeto}{contexto}debe ser un número positivo.")
 
 
def validar_numero(num: Union[int, float], nombre_campo: str = "", nombre_clase: str = ""):
    if not isinstance(num, (int, float)):
        sujeto = f"{nombre_campo} " if nombre_campo else "El valor "
        contexto = f"de {nombre_clase} " if nombre_clase else ""
        raise DatosInvalidosError(f"{sujeto}{contexto}debe ser un número.")
 
 
def validar_cadena_no_vacia(texto: str, nombre_campo: str = "", nombre_clase: str = ""):
    if not isinstance(texto, str) or not texto.strip():
        sujeto = f"{nombre_campo} " if nombre_campo else "El campo "
        contexto = f"de {nombre_clase} " if nombre_clase else ""
        raise DatosInvalidosError(f"{sujeto}{contexto}no puede estar vacío o contener solo espacios.")
 
 
def validar_datetime(fecha: datetime, nombre_campo: str = "", nombre_clase: str = ""):
    if not isinstance(fecha, datetime):
        sujeto = f"{nombre_campo} " if nombre_campo else "El campo "
        contexto = f"de {nombre_clase} " if nombre_clase else ""
        raise DatosInvalidosError(f"{sujeto}{contexto}debe ser un objeto de tipo datetime.")
 
 
def validar_instancia(objeto, clase_esperada, nombre_campo: str = "", nombre_clase: str = ""):
    if not isinstance(objeto, clase_esperada):
        sujeto = f"{nombre_campo} " if nombre_campo else "El objeto "
        contexto = f"de {nombre_clase} " if nombre_clase else ""
        raise DatosInvalidosError(f"{sujeto}{contexto}debe ser una instancia de la clase {clase_esperada.__name__}.")
 
 
def validar_booleano(valor, nombre_campo: str = "", nombre_clase: str = ""):
    if not isinstance(valor, bool):
        sujeto = f"{nombre_campo} " if nombre_campo else "El valor"
        contexto = f"de {nombre_clase} " if nombre_clase else ""
        raise DatosInvalidosError(f"{sujeto}{contexto}debe ser un valor booleano (True o False)")
 
 
def validar_time(hora, nombre_campo: str = "", nombre_clase: str = ""):
    if not isinstance(hora, time):
        sujeto = f"{nombre_campo} " if nombre_campo else "El campo "
        contexto = f"de {nombre_clase} " if nombre_clase else ""
        raise DatosInvalidosError(f"{sujeto}{contexto}debe ser un objeto de tipo time.")