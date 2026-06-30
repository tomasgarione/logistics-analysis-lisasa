import pytest
from datetime import time
from excepciones import DatosInvalidosError, CapacidadExcedidaError, VentanaHorariaError
from viaje import Viaje
from pedido import Pedido
from paquete import Paquete
from estadoviaje import EstadoViaje
from excepciones import EstadoViajeError

class TestViaje:
    def test_creacion_valida(self, viaje_furgoneta):
        assert viaje_furgoneta.estado == EstadoViaje.PLANIFICADO
        assert viaje_furgoneta.pedidos == []
 
    def test_id_vacio_falla(self, furgoneta, almacen_a, ruta_ab):
        with pytest.raises((ValueError, DatosInvalidosError)):
            Viaje("", furgoneta, almacen_a, ruta_ab, time(8, 53))
 
    def test_transporte_invalido_falla(self, almacen_a, ruta_ab):
        with pytest.raises((TypeError, DatosInvalidosError)):
            Viaje("VJ", "no soy transporte", almacen_a, ruta_ab, time(8, 53))
 
    def test_agregar_pedido_ok(self, viaje_furgoneta, pedido_base, paquete_liviano):
        pedido_base.agregar_paquete(paquete_liviano)
        viaje_furgoneta.agregar_pedido(pedido_base)
        assert len(viaje_furgoneta.pedidos) == 1
 
    def test_capacidad_peso_excedida(self, furgoneta, almacen_a, almacen_b, ruta_ab, cliente_base):
        viaje = Viaje("VJ-X", furgoneta, almacen_a, ruta_ab, time(8, 53))
        p1 = Pedido("PA", cliente_base, almacen_b, time(9, 0), time(18, 0))
        p1.agregar_paquete(Paquete("K1", 300.0, 1.0, "A"))
        p2 = Pedido("PB", cliente_base, almacen_b, time(9, 0), time(18, 0))
        p2.agregar_paquete(Paquete("K2", 300.0, 1.0, "B"))  # 600 kg > 500 max
        viaje.agregar_pedido(p1)
        with pytest.raises(CapacidadExcedidaError):
            viaje.agregar_pedido(p2)
 
    def test_ventana_horaria_incumplible(self, furgoneta, almacen_a, almacen_b, ruta_ab, cliente_base):
        viaje = Viaje("VJ-X", furgoneta, almacen_a, ruta_ab, time(8, 53))
        ped = Pedido("PI", cliente_base, almacen_b, time(7, 0), time(7, 30))
        ped.agregar_paquete(Paquete("KI", 1.0, 0.01, "X"))
        with pytest.raises(VentanaHorariaError):
            viaje.agregar_pedido(ped)
 
    def test_costo_total_furgoneta(self, viaje_furgoneta, pedido_base, paquete_liviano):
        pedido_base.agregar_paquete(paquete_liviano)
        viaje_furgoneta.agregar_pedido(pedido_base)
        assert viaje_furgoneta.obtener_costo_total() == pytest.approx(1280.0)  # 5km×156
 
    def test_impacto_ambiental_furgoneta(self, viaje_furgoneta, pedido_base, paquete_liviano):
        pedido_base.agregar_paquete(paquete_liviano)
        viaje_furgoneta.agregar_pedido(pedido_base)
        assert viaje_furgoneta.obtener_impacto_ambiental() == pytest.approx(0.75)  # 5×0.15

    def test_estado_inicial_es_planificado(self, viaje_furgoneta):
        assert viaje_furgoneta.estado == EstadoViaje.PLANIFICADO

    def test_iniciar_viaje(self, viaje_furgoneta):
        viaje_furgoneta.iniciar()
        assert viaje_furgoneta.estado == EstadoViaje.EN_CURSO

    def test_completar_viaje(self, viaje_furgoneta):
        viaje_furgoneta.iniciar()
        viaje_furgoneta.completar()
        assert viaje_furgoneta.estado == EstadoViaje.COMPLETADO

    def test_iniciar_dos_veces_falla(self, viaje_furgoneta):
        viaje_furgoneta.iniciar()
        with pytest.raises(EstadoViajeError):
            viaje_furgoneta.iniciar()

    def test_completar_sin_iniciar_falla(self, viaje_furgoneta):
        with pytest.raises(EstadoViajeError):
            viaje_furgoneta.completar()

    def test_agregar_pedido_en_curso_falla(self, viaje_furgoneta, pedido_base, paquete_liviano):
        pedido_base.agregar_paquete(paquete_liviano)
        viaje_furgoneta.iniciar()
        with pytest.raises(EstadoViajeError):
            viaje_furgoneta.agregar_pedido(pedido_base)