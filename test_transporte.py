from transporte import Transporte
from excepciones import DatosInvalidosError
import pytest
from furgoneta import Furgoneta
from camion import Camion
from motocicleta import Motocicleta
from mensajeroexterno import MensajeroExterno



class TestTransportes:
    def test_motocicleta_capacidades(self, moto):
        assert moto.peso_max == 100.0 and moto.volumen_max == 0.5

    def test_furgoneta_capacidades(self, furgoneta):
        assert furgoneta.peso_max == 500.0 and furgoneta.volumen_max == 10.0

    def test_camion_capacidades(self, camion):
        assert camion.peso_max == 5000.0 and camion.volumen_max == 30.0

    def test_patente_vacia_falla(self):
        with pytest.raises((DatosInvalidosError)):
            Motocicleta("", "Honda")

    def test_modelo_vacio_falla(self):
        with pytest.raises((DatosInvalidosError)):
            Furgoneta("F-01", "")

    def test_impacto_moto_menor_que_camion(self, moto, camion):
        assert moto.calcular_impacto_ambiental(10.0) < camion.calcular_impacto_ambiental(10.0)

    def test_costo_moto_menor_que_camion(self, moto, camion):
        distancia_km = 10
        num_pedidos = 1
        assert moto.calcular_costo(distancia_km, num_pedidos) < camion.calcular_costo(distancia_km, num_pedidos)

    def test_calcular_costo_moto(self, moto):
        assert moto.calcular_costo(10.0, 1) == pytest.approx(800.0)   # 10×80

    def test_calcular_costo_furgoneta(self, furgoneta):
        assert furgoneta.calcular_costo(10.0, 1) == pytest.approx(1560.0)  # 10×156

    def test_calcular_costo_camion(self, camion):
        assert camion.calcular_costo(10.0, 1) == pytest.approx(5000.0)  # 10×500

    def test_mensajero_costo_tarifa_fija(self, mensajero):
        assert mensajero.calcular_costo(999.0, 3) == pytest.approx(4500.0)

    def test_mensajero_costo_ignora_distancia(self, mensajero):
        assert mensajero.calcular_costo(1.0, 2) == mensajero.calcular_costo(9999.0, 2)

    def test_mensajero_impacto_cero(self, mensajero):
        assert mensajero.calcular_impacto_ambiental(100.0) == 0
