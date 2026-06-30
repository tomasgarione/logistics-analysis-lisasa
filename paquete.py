from validaciones import *

class Paquete():
    def __init__(self,id_paquete,peso,volumen,descripcion):
        validar_cadena_no_vacia(descripcion, "Descripción", Paquete)
        validar_cadena_no_vacia(id_paquete, "ID del paquete", Paquete)
        validar_numero_positivo(peso, "Peso", Paquete)
        validar_numero_positivo(volumen, "Volumen", Paquete)
        self.id = id_paquete
        self.peso = peso
        self.volumen = volumen
        self.descripcion = descripcion

    def __str__(self):
        return f"{self.descripcion} (Peso: {self.peso}, Volumen: {self.volumen})"
