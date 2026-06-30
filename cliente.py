from validaciones import *
 
class Cliente():
    def __init__(self, nombre, direccion, dni, telefono, mail):
        validar_cadena_no_vacia(nombre, "Nombre del cliente", "Cliente")
        validar_cadena_no_vacia(direccion, "Dirección del cliente", "Cliente")
        validar_cadena_no_vacia(dni, "DNI del cliente", "Cliente")
        validar_cadena_no_vacia(telefono, "Teléfono del cliente", "Cliente")
        validar_cadena_no_vacia(mail, "Mail del cliente", "Cliente")
        self.nombre = nombre
        self.direccion = direccion
        self.dni = dni
        self.telefono = telefono
        self.mail = mail
 
    def __eq__(self, other):
        if not isinstance(other, Cliente):
            return NotImplemented
        return self.dni == other.dni
 
    def __hash__(self):
        return hash(self.dni)
 
    def __str__(self):
        return f"Cliente: {self.nombre}, Dirección: {self.direccion}, DNI: {self.dni}, Teléfono: {self.telefono}, Mail: {self.mail}"
 
    def __repr__(self):
        return (
            f"Cliente(nombre={self.nombre!r}, "
            f"dni={self.dni!r}, "
            f"mail={self.mail!r})"
        )