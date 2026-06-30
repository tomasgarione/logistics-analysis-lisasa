import pytest
from cliente import Cliente
from excepciones import DatosInvalidosError
 
 
class TestCliente:
    def test_creacion_valida(self):
        c = Cliente("Ana", "Calle 1", "12345678", "11-1234", "ana@mail.com")
        assert c.nombre == "Ana"
 
    def test_nombre_vacio_falla(self):
        with pytest.raises(DatosInvalidosError):
            Cliente("", "Calle 1", "12345678", "11-1234", "ana@mail.com")
 
    def test_dni_vacio_falla(self):
        with pytest.raises(DatosInvalidosError):
            Cliente("Ana", "Calle 1", "", "11-1234", "ana@mail.com")
 
    def test_mail_vacio_falla(self):
        with pytest.raises(DatosInvalidosError):
            Cliente("Ana", "Calle 1", "12345678", "11-1234", "")
 
    def test_telefono_vacio_falla(self):
        with pytest.raises(DatosInvalidosError):
            Cliente("Ana", "Calle 1", "12345678", "", "ana@mail.com")
 
    # --- igualdad por DNI ---
 
    def test_mismo_dni_son_iguales(self):
        c1 = Cliente("Juan Pérez", "Calle Falsa 123", "30111222", "11-1234", "juan@mail.com")
        c2 = Cliente("Juan Pérez", "Calle Falsa 123", "30111222", "11-1234", "juan@mail.com")
        assert c1 == c2
 
    def test_distinto_dni_no_son_iguales(self):
        c1 = Cliente("Ana", "Calle 1", "11111111", "11-1234", "ana@mail.com")
        c2 = Cliente("Ana", "Calle 1", "22222222", "11-1234", "ana@mail.com")
        assert c1 != c2
 
    def test_cliente_en_lista_por_dni(self):
        c1 = Cliente("Juan", "Calle 1", "30111222", "11-1234", "juan@mail.com")
        c2 = Cliente("Juan", "Calle 1", "30111222", "11-1234", "juan@mail.com")
        clientes = [c1]
        assert c2 in clientes
 
    def test_cliente_en_set_por_dni(self):
        c1 = Cliente("Juan", "Calle 1", "30111222", "11-1234", "juan@mail.com")
        c2 = Cliente("Juan", "Calle 1", "30111222", "11-1234", "juan@mail.com")
        assert len({c1, c2}) == 1
 
    def test_comparacion_con_no_cliente_devuelve_not_implemented(self):
        c = Cliente("Ana", "Calle 1", "12345678", "11-1234", "ana@mail.com")
        assert c.__eq__("no soy cliente") == NotImplemented