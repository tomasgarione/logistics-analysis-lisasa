import pytest
from comprobante import Comprobante
from estadopedido import EstadoPedido
from excepciones import DatosInvalidosError, EstadoPedidoError


class TestComprobante:
    def test_generar_desde_en_camino(self, pedido_base, paquete_liviano):
        pedido_base.agregar_paquete(paquete_liviano)
        pedido_base.avanzar_estado()
        comp = Comprobante.generar(pedido_base, "María García")
        assert comp.receptor == "María García"
        assert pedido_base.estado == EstadoPedido.ENTREGADO

    def test_generar_desde_pendiente_falla(self, pedido_base):
        with pytest.raises(EstadoPedidoError):
            Comprobante.generar(pedido_base, "Receptor")

    def test_generar_desde_entregado_falla(self, pedido_base, paquete_liviano):
        pedido_base.agregar_paquete(paquete_liviano)
        pedido_base.avanzar_estado()
        pedido_base.avanzar_estado()
        with pytest.raises(EstadoPedidoError):
            Comprobante.generar(pedido_base, "Receptor")

    def test_receptor_vacio_falla(self, pedido_base, paquete_liviano):
        pedido_base.agregar_paquete(paquete_liviano)
        pedido_base.avanzar_estado()
        with pytest.raises((ValueError, DatosInvalidosError)):
            Comprobante.generar(pedido_base, "")

    def test_id_incluye_id_pedido(self, pedido_base, paquete_liviano):
        pedido_base.agregar_paquete(paquete_liviano)
        pedido_base.avanzar_estado()
        comp = Comprobante.generar(pedido_base, "Juan")
        assert "PED-001" in comp.id_comprobante

    def test_fecha_hora_registrada(self, pedido_base, paquete_liviano):
        pedido_base.agregar_paquete(paquete_liviano)
        pedido_base.avanzar_estado()
        comp = Comprobante.generar(pedido_base, "Juan")
        assert comp.fecha_hora is not None
