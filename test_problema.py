import pytest
from problema import Problema, TipoProblema
from excepciones import DatosInvalidosError

class TestProblema:
    def test_creacion_valida(self, pedido_base):
        p = Problema(TipoProblema.DANO, "Paquete roto", pedido_base)
        assert p.tipo == TipoProblema.DANO and p.pedido_afectado == pedido_base

    def test_tipo_invalido_falla(self):
        with pytest.raises((ValueError, DatosInvalidosError, TypeError)):
            Problema("NO_ES_ENUM", "desc")

    def test_descripcion_vacia_falla(self):
        with pytest.raises((ValueError, DatosInvalidosError)):
            Problema(TipoProblema.RETRASO, "")

    def test_fecha_default_asignada(self):
        p = Problema(TipoProblema.AUSENTE, "No estaba")
        assert p.fecha is not None

    def test_todos_los_tipos_validos(self):
        for tipo in TipoProblema:
            assert Problema(tipo, f"Test {tipo.name}").tipo == tipo

    def test_str_contiene_tipo_y_descripcion(self):
        p = Problema(TipoProblema.DANO, "Caja rota")
        assert "DAÑO" in str(p) and "Caja rota" in str(p)

