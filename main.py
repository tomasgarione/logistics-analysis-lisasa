from sistema import Sistema
from almacen import Almacen
from cliente import Cliente
from pedido import Pedido
from ruta import Ruta
from motocicleta import Motocicleta
from furgoneta import Furgoneta
from camion import Camion
from mensajeroexterno import MensajeroExterno
from datetime import time
from paquete import Paquete
from comprobante import Comprobante
from problema import Problema, TipoProblema
from analizador import AnalizadorOperaciones
 
# ─────────────────────────────────────────────────────────────────────────────
# Helpers de presentación
# ─────────────────────────────────────────────────────────────────────────────
 
def separador(titulo=""):
    linea = "─" * 60
    if titulo:
        print(f"\n{linea}\n  {titulo}\n{linea}")
    else:
        print(linea)
 
 
# ─────────────────────────────────────────────────────────────────────────────
# FASE 1 — Inicialización del sistema
# ─────────────────────────────────────────────────────────────────────────────
 
def fase_inicializacion(lisasa):
    separador("FASE 1 · Inicialización del sistema")
 
    # Almacenes con coordenadas (x, y) en km
    alm_central = Almacen("ALM-01", "Central BsAs",   "Av. Corrientes 1234", 0.0,  0.0)
    alm_norte   = Almacen("ALM-02", "Depósito Norte", "Av. Santa Fe 2000",   5.0,  8.0)
    alm_sur     = Almacen("ALM-03", "Depósito Sur",   "Av. Rivadavia 5000",  12.0, 3.0)
    alm_oeste   = Almacen("ALM-04", "Depósito Oeste", "Av. Libertador 3000", 7.0,  10.0)
 
    for alm in [alm_central, alm_norte, alm_sur, alm_oeste]:
        lisasa.cargar_almacen(alm)
    print(f"  ✓ {len(lisasa.almacenes)} almacenes cargados.")
 
    # Flota: 3 de cada tipo + 1 mensajero externo
    for i in range(1, 4):
        lisasa.cargar_transporte(Motocicleta(f"MOTO-00{i}", "Honda Titan"))
        lisasa.cargar_transporte(Furgoneta(f"FURG-00{i}",  "Renault Kangoo"))
        lisasa.cargar_transporte(Camion(f"CAMI-00{i}",     "Mercedes Benz"))
    lisasa.cargar_transporte(MensajeroExterno("MENS-001", "Rappi Express"))
    print(f"  ✓ {len(lisasa.transportes)} vehículos cargados.")
 
    # Rutas — tiempos de llegada calculados a 40 km/h:
    #   Ruta-01 [Central→Norte→Sur]   salida 8:46 → Norte 9:00, Sur  9:13
    #   Ruta-02 [Central→Oeste→Sur]   salida 8:42 → Oeste 9:00, Sur  9:13
    #   Ruta-03 [Central→Norte→Oeste] salida 8:46 → Norte 9:00, Oeste 9:04
    ruta_1 = Ruta("Ruta-01", [alm_central, alm_norte, alm_sur],   velocidad_km_h=40.0)
    ruta_2 = Ruta("Ruta-02", [alm_central, alm_oeste, alm_sur],   velocidad_km_h=40.0)
    ruta_3 = Ruta("Ruta-03", [alm_central, alm_norte, alm_oeste], velocidad_km_h=40.0)
 
    # índice 3 = FURG-001, índice 6 = CAMI-001, índice 0 = MOTO-001, índice 9 = MENS-001
    lisasa.cargar_nuevo_viaje(lisasa.transportes[1], alm_central, ruta_1, time(8, 46))
    lisasa.cargar_nuevo_viaje(lisasa.transportes[2], alm_central, ruta_2, time(8, 42))
    lisasa.cargar_nuevo_viaje(lisasa.transportes[0], alm_central, ruta_3, time(8, 46))
    lisasa.cargar_nuevo_viaje(lisasa.transportes[9], alm_central, ruta_1, time(8, 46))
    print(f"  ✓ {len(lisasa.viajes)} viajes planificados.")
 
    return alm_norte, alm_sur, alm_oeste
 
 
# ─────────────────────────────────────────────────────────────────────────────
# FASE 2 — Carga de pedidos
# ─────────────────────────────────────────────────────────────────────────────
 
def fase_carga_pedidos(lisasa, alm_norte, alm_sur, alm_oeste):
    separador("FASE 2 · Carga de pedidos")
 
    juan   = Cliente("Juan Pérez",   "Calle Falsa 123",     "30111222", "1122334455", "juan@mail.com")
    ana    = Cliente("Ana García",   "Av. Siempre Viva 42", "28999111", "1133445566", "ana@mail.com")
    carlos = Cliente("Carlos López", "Rivadavia 800",       "35123456", "1144556677", "carlos@mail.com")
 
    # PED-001 → Furgoneta · Ruta-01 · destino Norte (llega 9:00)
    ped_1 = Pedido("PED-001", juan,   alm_norte, time(9,  0), time(12, 0))
    ped_1.agregar_paquete(Paquete("PKG-001", 15.0, 0.3, "Electrodoméstico"))
    ped_1.agregar_paquete(Paquete("PKG-002",  8.0, 0.2, "Accesorios"))
 
    # PED-002 → Furgoneta · Ruta-01 · destino Sur (llega 9:13)
    ped_2 = Pedido("PED-002", ana,    alm_sur,   time(9, 10), time(13, 0))
    ped_2.agregar_paquete(Paquete("PKG-003", 200.0, 4.0, "Mobiliario"))
 
    # PED-003 → Camion · Ruta-02 · destino Oeste (llega 9:00)
    ped_3 = Pedido("PED-003", carlos, alm_oeste, time(9,  0), time(11, 0))
    ped_3.agregar_paquete(Paquete("PKG-004",  80.0, 2.0, "Maquinaria liviana"))
    ped_3.agregar_paquete(Paquete("PKG-005",  50.0, 1.5, "Repuestos"))
 
    # PED-004 → Camion · Ruta-02 · destino Sur (llega 9:13) — carga pesada
    ped_4 = Pedido("PED-004", ana,    alm_sur,   time(9, 10), time(15, 0))
    ped_4.agregar_paquete(Paquete("PKG-006", 3000.0, 18.0, "Carga industrial"))
 
    # PED-005 → Moto · Ruta-03 · destino Norte (llega 9:00) — paquete pequeño
    ped_5 = Pedido("PED-005", juan,   alm_norte, time(9,  0), time(10, 0))
    ped_5.agregar_paquete(Paquete("PKG-007", 2.0, 0.05, "Documentos"))
 
    # PED-006 → Moto · Ruta-03 · destino Oeste (llega 9:04)
    ped_6 = Pedido("PED-006", carlos, alm_oeste, time(9,  0), time(10, 0))
    ped_6.agregar_paquete(Paquete("PKG-008", 3.0, 0.08, "Repuesto pequeño"))
 
    # PED-URG → Mensajero · Ruta-01 · destino Norte — urgente
    ped_urg = Pedido("PED-URG", juan, alm_norte, time(9, 0), time(18, 0), urgente=True)
    ped_urg.agregar_paquete(Paquete("PKG-URG", 1.0, 0.02, "Documento urgente"))
 
    for ped in [ped_1, ped_2, ped_3, ped_4, ped_5, ped_6, ped_urg]:
        lisasa.cargar_pedido(ped)
 
    print(f"  ✓ {len(lisasa.pedidos)} pedidos cargados:")
    for p in lisasa.pedidos:
        urg = " [URGENTE]" if p.urgente else ""
        print(f"    · {p.id_pedido}{urg:<10} → {p.destino.nombre:<18} "
              f"{p.calcular_peso_total():.1f} kg / {p.calcular_volumen_total():.2f} m³  "
              f"franja {p.franja_inicio.strftime('%H:%M')}–{p.franja_fin.strftime('%H:%M')}")
 
 
# ─────────────────────────────────────────────────────────────────────────────
# FASE 3 — Procesamiento de pedidos
# ─────────────────────────────────────────────────────────────────────────────
 
def fase_procesamiento(lisasa):
    separador("FASE 3 · Procesamiento automático de pedidos")

    # Corre fluidamente: desencola un pedido por vuelta hasta vaciar la lista principal
    while lisasa.pedidos:
        res = lisasa.procesar_siguiente_pedido()
        if res is None:
            print("  No hay pedidos para procesar.")
            break
    
        tipo_urgencia = "URGENTE" if res["urgente"] else "normal"
        print(f"\n  Procesando {res['pedido_id']} → {res['destino_nombre']} ({tipo_urgencia})")

        for evento in res["eventos"]:
                tipo_evento = evento[0]
                
                if tipo_evento == "sin_viajes":
                    print(f"    ✗ Sin viajes compatibles para {evento[1]}.")
                elif tipo_evento == "asignado":
                    print(f"    ✓ Asignado a {evento[1]} ({evento[2]} {evento[3]}). Estado: {evento[4]}")
                elif tipo_evento == "rechazo_estado_viaje":
                    print(f"    · {evento[1]} rechazó por estado del viaje incompatible.")
                elif tipo_evento == "rechazo_capacidad":
                    print(f"    · {evento[1]} rechazó por capacidad excedida.")
                elif tipo_evento == "rechazo_ventana":
                    print(f"    · {evento[1]} rechazó por ventana horaria incompatible.")
                elif tipo_evento == "no_asignado":
                    print(f"    ✗ No se pudo asignar {evento[1]} a ningún viaje.")  

    # Al terminar la jornada, reportamos ordenadamente los saldos del depósito
    if lisasa.pedidos_no_asignados:
        print(f"\n  [REPORTE] El proceso terminó. {len(lisasa.pedidos_no_asignados)} pedido(s) quedaron retenido(s) en depósito:")
        for p in lisasa.pedidos_no_asignados:
            print(f"            - {p.id_pedido} con destino a {p.destino.nombre}")
    else:
        print("\n  ✓ ¡Día perfecto! Todos los pedidos de la cola se asignaron con éxito.")
 
# ─────────────────────────────────────────────────────────────────────────────
# FASE 4 — Entrega y comprobantes
# ─────────────────────────────────────────────────────────────────────────────
 
def fase_entregas(lisasa):
    separador("FASE 4 · Ejecución de entregas y comprobantes")
 
    receptores = {
        "PED-001": "María Torres",
        "PED-002": "Roberto Silva",
        "PED-003": "Laura Méndez",
        "PED-004": "Diego Ruiz",
        "PED-005": "Sofía Castro",
        "PED-006": "Tomás Vega",
        "PED-URG": "Valentina Ríos",
    }
 
    comprobantes = []
    for viaje in lisasa.viajes:
        if not viaje.pedidos:
            continue
        print(f"\n  {viaje.id_viaje} · {viaje.transporte.__class__.__name__} "
              f"({viaje.transporte.patente}):")
        
        viaje.iniciar()  # Cambia el estado a EN_CURSO
        for pedido in viaje.pedidos:
            receptor = receptores.get(pedido.id_pedido, "Receptor")
            try:
                comp = Comprobante.generar(pedido, receptor)
                comprobantes.append(comp)
                print(f"    ✓ {comp}")
            except Exception as e:
                print(f"    ✗ {pedido.id_pedido}: {e}")
        viaje.completar()  # Cambia el estado a COMPLETADO
    return comprobantes
 
 
# ─────────────────────────────────────────────────────────────────────────────
# FASE 5 — Registro de incidencias
# ─────────────────────────────────────────────────────────────────────────────
 
def fase_incidencias(lisasa):
    separador("FASE 5 · Registro de incidencias")
 
    pedidos_por_id = {
        p.id_pedido: p
        for viaje in lisasa.viajes
        for p in viaje.pedidos
    }
 
    incidencias = [
        ("PED-002", TipoProblema.DANO,    "Caja de mobiliario llegó aplastada por mal embalaje"),
        ("PED-003", TipoProblema.RETRASO, "Tráfico en Av. Libertador, 20 min de demora"),
        ("PED-005", TipoProblema.AUSENTE, "Cliente no estaba en el domicilio al momento de entrega"),
    ]
 
    for id_ped, tipo, descripcion in incidencias:
        if id_ped in pedidos_por_id:
            pedido = pedidos_por_id[id_ped]
            pedido.agregar_incidencia(Problema(tipo, descripcion, pedido))
            print(f"  ⚠  {id_ped} · [{tipo.value}] {descripcion}")
 
 
# ─────────────────────────────────────────────────────────────────────────────
# FASE 6 — Análisis operacional
# ─────────────────────────────────────────────────────────────────────────────
 
def fase_analisis(lisasa):
    separador("FASE 6 · Análisis operacional")
 
    todos_los_pedidos = [p for viaje in lisasa.viajes for p in viaje.pedidos]
    analizador = AnalizadorOperaciones(
        pedidos=todos_los_pedidos,
        transportes=lisasa.transportes
    )
 
    graves = analizador.filtrar_incidencias_graves()
    print(f"\n  Incidencias graves (DAÑO): {len(graves)}")
    for desc in graves:
        print(f"    · {desc}")
 
    ruta_csv = "incidencias_graves.csv"
    resultado_exportacion = analizador.exportar_incidencias_csv(ruta_csv)
    if resultado_exportacion:
        print(f"  ✓ CSV generado: {ruta_csv} ({len(graves)} filas).")
    else:
        print("  No hay incidencias graves para exportar")
 
    print(f"\n  Ajuste por inflación ({analizador.PORCENTAJE_INFLACION*100:.0f}%):")
    costos_ajustados = analizador.ajustar_costos_por_inflacion()
    for transporte, costo_nuevo in zip(lisasa.transportes, costos_ajustados):
        print(f"    · {transporte.patente:<12} {transporte.__class__.__name__:<18} "
              f"${transporte.costo_base_km:.2f}/km → ${costo_nuevo:.2f}/km")
 
 
# ─────────────────────────────────────────────────────────────────────────────
# FASE 7 — Resumen del día
# ─────────────────────────────────────────────────────────────────────────────
 
def fase_resumen(lisasa):
    separador("FASE 7 · Resumen del día operativo")
 
    costo_total   = 0.0
    emision_total = 0.0
    total_entregados = 0
 
    for viaje in lisasa.viajes:
        if not viaje.pedidos:
            continue
        costo   = viaje.obtener_costo_total()
        emision = viaje.obtener_impacto_ambiental()
        distancia = viaje.ruta.calcular_distancia_total()
        costo_total   += costo
        emision_total += emision
        total_entregados += len(viaje.pedidos)
 
        print(f"\n  {viaje.id_viaje} · {viaje.transporte.__class__.__name__} "
              f"({viaje.transporte.patente})")
        print(f"    Pedidos entregados : {len(viaje.pedidos)}")
        print(f"    Distancia total    : {distancia:.2f} km")
        print(f"    Costo operativo    : ${costo:,.2f}")
        print(f"    Emisiones CO₂      : {emision:.2f} kg")
 
    separador()
    print(f"  Total pedidos entregados : {total_entregados}")
    print(f"  Total pedidos pendientes : {len(lisasa.pedidos_no_asignados)}")
    print(f"  Costo total del día      : ${costo_total:,.2f}")
    print(f"  Emisiones totales        : {emision_total:.2f} kg CO₂")
    separador()
 
 
# ─────────────────────────────────────────────────────────────────────────────
# PUNTO DE ENTRADA
# ─────────────────────────────────────────────────────────────────────────────
 
def main():
    print("=" * 60)
    print("   LOGÍSTICA INTELIGENTE S.A. — Sistema de Operaciones")
    print("=" * 60)
 
    lisasa = Sistema()
 
    alm_norte, alm_sur, alm_oeste = fase_inicializacion(lisasa)
    fase_carga_pedidos(lisasa, alm_norte, alm_sur, alm_oeste)
    fase_procesamiento(lisasa)
    fase_entregas(lisasa)
    fase_incidencias(lisasa)
    fase_analisis(lisasa)
    fase_resumen(lisasa)
 
    print("\n  Sistema LISASA finalizado correctamente.\n")
 
 
if __name__ == "__main__":
    main()