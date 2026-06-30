import pytest
from ruta import Ruta
from excepciones import DatosInvalidosError
from almacen import Almacen
from pedido import Pedido
from cliente import Cliente
from datetime import time

class TestRuta:
    def test_distancia_total(self, ruta_ab):
        assert ruta_ab.calcular_distancia_total() == pytest.approx(5.0)

    def test_incluye_almacen_verdadero(self, ruta_ab, almacen_b):
        assert ruta_ab.incluye_almacen(almacen_b) is True

    def test_incluye_almacen_falso(self, ruta_ab):
        otro = Almacen("ALM-99", "Lejano", "Calle X", 100.0, 100.0)
        assert ruta_ab.incluye_almacen(otro) is False

    def test_ruta_con_un_almacen_falla(self, almacen_a):
        with pytest.raises(DatosInvalidosError):
            Ruta("R", [almacen_a])

    def test_ruta_sin_almacenes_falla(self):
        with pytest.raises(DatosInvalidosError):
            Ruta("R", [])

    def test_ventana_llega_a_tiempo(self, ruta_ab, pedido_base):
        # Sale 08:53 → llega 09:01 ∈ [09:00, 18:00] ✓
        assert ruta_ab.verificar_ventana(pedido_base, time(8, 53)) is True

    def test_ventana_llega_muy_temprano(self, ruta_ab, pedido_base):
        # Sale 08:00 → llega 08:07, antes de franja_inicio 09:00 ✗
        assert ruta_ab.verificar_ventana(pedido_base, time(8, 0)) is False

    def test_ventana_destino_no_en_ruta(self, ruta_ab, almacen_a, cliente_base):
        fuera = Almacen("ALM-99", "Lejano", "Calle Z", 99.0, 99.0)
        ped = Pedido("P", cliente_base, fuera, time(9, 0), time(18, 0))
        assert ruta_ab.verificar_ventana(ped, time(8, 53)) is False
