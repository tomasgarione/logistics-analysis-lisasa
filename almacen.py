from validaciones import *

class Almacen():
    def __init__(self,id_almacen,nombre,ubicacion,x,y):
        validar_cadena_no_vacia(id_almacen, "ID del almacén", "Almacén")
        validar_cadena_no_vacia(nombre, "Nombre del almacén", "Almacén")
        validar_cadena_no_vacia(ubicacion, "Ubicación del almacén", "Almacén")
        validar_numero(x, "Coordenada X del almacén", "Almacén")
        validar_numero(y, "Coordenada Y del almacén", "Almacén")
        self.id_almacen = id_almacen
        self.nombre = nombre
        self.ubicacion = ubicacion
        self.x = x
        self.y = y
    
    def __eq__(self, other):
        if not isinstance(other, Almacen):
            return NotImplemented
        return self.id_almacen == other.id_almacen

    def __hash__(self):
        return hash(self.id_almacen)
    
    def __str__(self):
        return (
            f"Almacén(ID: {self.id_almacen}, Nombre: {self.nombre}, "
            f"Ubicación: {self.ubicacion}, Coordenadas: ({self.x}, {self.y}))"
        )
