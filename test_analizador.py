import pytest
from analizador import AnalizadorOperaciones
from problema import Problema, TipoProblema
from excepciones import DatosInvalidosError
from mensajeroexterno import MensajeroExterno
 
class TestAnalizador:
    @pytest.fixture
    def pedido_con_incidencias(self, pedido_base, paquete_liviano):
        pedido_base.agregar_paquete(paquete_liviano)
        pedido_base.agregar_incidencia(Problema(TipoProblema.DANO,    "Caja aplastada", pedido_base))
        pedido_base.agregar_incidencia(Problema(TipoProblema.RETRASO, "Tráfico",        pedido_base))
        return pedido_base
 
    def test_filtrar_graves_solo_dano(self, pedido_con_incidencias):
        analizador = AnalizadorOperaciones(pedidos=[pedido_con_incidencias])
        graves = analizador.filtrar_incidencias_graves()
        assert len(graves) == 1 and "Caja aplastada" in graves
 
    def test_retraso_no_es_grave(self, pedido_con_incidencias):
        analizador = AnalizadorOperaciones(pedidos=[pedido_con_incidencias])
        graves = analizador.filtrar_incidencias_graves()
        assert not any("Tráfico" in g for g in graves)
 
    def test_sin_incidencias_graves_devuelve_vacio(self, pedido_base, paquete_liviano):
        pedido_base.agregar_paquete(paquete_liviano)
        pedido_base.agregar_incidencia(Problema(TipoProblema.RETRASO, "Tráfico", pedido_base))
        assert AnalizadorOperaciones(pedidos=[pedido_base]).filtrar_incidencias_graves() == []
 
    def test_sin_pedidos_devuelve_vacio(self):
        assert AnalizadorOperaciones().filtrar_incidencias_graves() == []

    def test_ajuste_inflacion_devuelve_tuplas(self, moto, furgoneta, camion):
        ajustados = AnalizadorOperaciones(transportes=[moto, furgoneta, camion]).ajustar_costos_por_inflacion()
        patentes = [patente for patente, _ in ajustados]
        assert "MOTO-001" in patentes
        assert "FURG-001" in patentes
        assert "CAMI-001" in patentes
 
    def test_ajuste_inflacion_valores(self, moto, furgoneta, camion):
        ajustados = AnalizadorOperaciones(transportes=[moto, furgoneta, camion]).ajustar_costos_por_inflacion()
        costos = {patente: costo for patente, costo in ajustados}
        assert costos["MOTO-001"] == pytest.approx(80.0  * 1.15)
        assert costos["FURG-001"] == pytest.approx(120.0 * 1.15)
        assert costos["CAMI-001"] == pytest.approx(200.0 * 1.15)
 
    def test_ajuste_excluye_mensajero_externo(self, moto, mensajero):
        # MensajeroExterno no debe aparecer en el resultado
        ajustados = AnalizadorOperaciones(transportes=[moto, mensajero]).ajustar_costos_por_inflacion()
        patentes = [patente for patente, _ in ajustados]
        assert mensajero.patente not in patentes
        assert moto.patente in patentes
 
    def test_ajuste_solo_mensajero_devuelve_vacio(self, mensajero):
        ajustados = AnalizadorOperaciones(transportes=[mensajero]).ajustar_costos_por_inflacion()
        assert ajustados == []
 
    def test_ajuste_no_muta_objeto(self, moto):
        costo_original = moto.costo_base_km
        AnalizadorOperaciones(transportes=[moto]).ajustar_costos_por_inflacion()
        assert moto.costo_base_km == costo_original
 
    # --- exportar CSV ---
 
    def test_exportar_csv_genera_archivo(self, pedido_con_incidencias, tmp_path):
        analizador = AnalizadorOperaciones(pedidos=[pedido_con_incidencias])
        ruta_csv = tmp_path / "inc.csv"
        assert analizador.exportar_incidencias_csv(str(ruta_csv)) is not None
        assert ruta_csv.exists()
 
    def test_exportar_csv_sin_graves_devuelve_none(self, pedido_base, paquete_liviano, tmp_path):
        pedido_base.agregar_paquete(paquete_liviano)
        pedido_base.agregar_incidencia(Problema(TipoProblema.RETRASO, "Solo retraso", pedido_base))
        analizador = AnalizadorOperaciones(pedidos=[pedido_base])
        assert analizador.exportar_incidencias_csv(str(tmp_path / "v.csv")) is None