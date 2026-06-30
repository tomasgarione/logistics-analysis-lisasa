import pytest
from almacen import Almacen
from excepciones import DatosInvalidosError

class TestAlmacen:
    def test_creacion_valida(self):
        a = Almacen("ALM-01", "Central", "Av. Siempre Viva", 0.0, 0.0)
        assert a.id_almacen == "ALM-01"

    def test_id_vacio_falla(self):
        with pytest.raises((DatosInvalidosError)):
            Almacen("", "Central", "Calle 1", 0.0, 0.0)

    def test_nombre_vacio_falla(self):
        with pytest.raises((DatosInvalidosError)):
            Almacen("ALM-01", "", "Calle 1", 0.0, 0.0)

    def test_ubicacion_vacia_falla(self):
        with pytest.raises((DatosInvalidosError)):
            Almacen("ALM-01", "Central", "", 0.0, 0.0)

    def test_coordenada_no_numerica_falla(self):
        with pytest.raises((DatosInvalidosError)):
            Almacen("ALM-01", "Central", "Calle 1", "abc", 0.0)
