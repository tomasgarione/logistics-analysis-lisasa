import pytest
from pedido import Pedido
from estadopedido import EstadoPedido
from excepciones import DatosInvalidosError, EstadoPedidoError
from datetime import time
from problema import Problema, TipoProblema
 
class TestPedido:
    def test_creacion_valida(self, pedido_base):
        assert pedido_base.id_pedido == "PED-001"
        assert pedido_base.estado == EstadoPedido.PENDIENTE
        assert pedido_base.urgente is False
 
    def test_id_vacio_falla(self, cliente_base, almacen_b):
        with pytest.raises(( DatosInvalidosError)):
            Pedido("", cliente_base, almacen_b, time(9, 0), time(18, 0))
 
    def test_cliente_invalido_falla(self, almacen_b):
        with pytest.raises((DatosInvalidosError)):
            Pedido("P", "no soy cliente", almacen_b, time(9, 0), time(18, 0))
 
    def test_destino_invalido_falla(self, cliente_base):
        with pytest.raises((DatosInvalidosError)):
            Pedido("P", cliente_base, "no soy almacen", time(9, 0), time(18, 0))
 
    def test_agregar_paquete(self, pedido_base, paquete_liviano):
        pedido_base.agregar_paquete(paquete_liviano)
        assert len(pedido_base.paquetes) == 1
 
    def test_paquete_invalido_falla(self, pedido_base):
        with pytest.raises((DatosInvalidosError)):
            pedido_base.agregar_paquete("no soy paquete")
 
    def test_calcular_peso_total(self, pedido_base, paquete_liviano, paquete_pesado):
        pedido_base.agregar_paquete(paquete_liviano)   # 5 kg
        pedido_base.agregar_paquete(paquete_pesado)    # 90 kg
        assert pedido_base.calcular_peso_total() == pytest.approx(95.0)
 
    def test_calcular_volumen_total(self, pedido_base, paquete_liviano, paquete_pesado):
        pedido_base.agregar_paquete(paquete_liviano)   # 0.1
        pedido_base.agregar_paquete(paquete_pesado)    # 0.4
        assert pedido_base.calcular_volumen_total() == pytest.approx(0.5)
 
    def test_peso_cero_sin_paquetes(self, pedido_base):
        assert pedido_base.calcular_peso_total() == 0.0
 
    def test_avanzar_pendiente_a_en_camino(self, pedido_base):
        pedido_base.avanzar_estado()
        assert pedido_base.estado == EstadoPedido.EN_CAMINO
 
    def test_avanzar_en_camino_a_entregado(self, pedido_base):
        pedido_base.avanzar_estado()
        pedido_base.avanzar_estado()
        assert pedido_base.estado == EstadoPedido.ENTREGADO
 
    def test_avanzar_desde_final_falla(self, pedido_base):
        pedido_base.avanzar_estado()
        pedido_base.avanzar_estado()
        with pytest.raises(EstadoPedidoError):
            pedido_base.avanzar_estado()
 
    def test_agregar_incidencia(self, pedido_base):
        prob = Problema(TipoProblema.RETRASO, "Tráfico", pedido_base)
        pedido_base.agregar_incidencia(prob)
        assert len(pedido_base.incidencias) == 1
 
    def test_franja_horaria_invalida_falla(self, cliente_base, almacen_b):
        with pytest.raises(DatosInvalidosError):
            Pedido("P", cliente_base, almacen_b, time(18, 0), time(9, 0))
 
    def test_franja_horaria_igual_falla(self, cliente_base, almacen_b):
        with pytest.raises(DatosInvalidosError):
            Pedido("P", cliente_base, almacen_b, time(10, 0), time(10, 0))