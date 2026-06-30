from paquete import Paquete
from excepciones import DatosInvalidosError
import pytest

class TestPaquete:
    def test_creacion_valida(self):
        p = Paquete("PKG-01", 10.0, 0.5, "Laptop")
        assert p.id == "PKG-01" and p.peso == 10.0 and p.volumen == 0.5

    def test_peso_negativo_falla(self):
        with pytest.raises((DatosInvalidosError)):
            Paquete("P", -1.0, 0.5, "X")

    def test_peso_cero_falla(self):
        with pytest.raises((DatosInvalidosError)):
            Paquete("P", 0.0, 0.5, "X")

    def test_volumen_negativo_falla(self):
        with pytest.raises((DatosInvalidosError)):
            Paquete("P", 5.0, -0.1, "X")

    def test_id_vacio_falla(self):
        with pytest.raises((DatosInvalidosError)):
            Paquete("", 5.0, 0.1, "X")

    def test_descripcion_vacia_falla(self):
        with pytest.raises((DatosInvalidosError)):
            Paquete("P", 5.0, 0.1, "")

    def test_str_contiene_descripcion(self):
        assert "Laptop" in str(Paquete("P", 10.0, 0.5, "Laptop"))