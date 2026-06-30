import pytest
from estadopedido import EstadoPedido

class TestEstadoPedido:
    def test_siguiente_pendiente(self):
        assert EstadoPedido.PENDIENTE.siguiente() == EstadoPedido.EN_CAMINO

    def test_siguiente_en_camino(self):
        assert EstadoPedido.EN_CAMINO.siguiente() == EstadoPedido.ENTREGADO

    def test_siguiente_entregado_es_none(self):
        assert EstadoPedido.ENTREGADO.siguiente() is None
