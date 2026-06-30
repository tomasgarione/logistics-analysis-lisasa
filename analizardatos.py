import csv
import numpy as np
import matplotlib.pyplot as plt

def cargar_datos():
    solicitudes, incidencias, vehiculos = [], [], []
    with open("dataset_solicitudes.csv", "r", encoding="utf-8") as f:
        for row in csv.DictReader(f): solicitudes.append(row)
    with open("dataset_incidencias.csv", "r", encoding="utf-8") as f:
        for row in csv.DictReader(f): incidencias.append(row)
    with open("dataset_vehiculos.csv", "r", encoding="utf-8") as f:
        for row in csv.DictReader(f): vehiculos.append(row)
    return solicitudes, incidencias, vehiculos

def analizar_costos_por_zona(solicitudes):
    print("\n--- ANÁLISIS DE COSTOS OPERATIVOS ---")
    
    # 1. Extraemos todos los datos necesarios en arrays de NumPy
    zonas = np.array([s['zona_destino'] for s in solicitudes])
    costos = np.array([float(s['costo_viaje']) for s in solicitudes])
    distancias = np.array([float(s['distancia_km']) for s in solicitudes])
    pesos = np.array([float(s['peso_kg']) for s in solicitudes])
    depositos = np.array([s['deposito_origen'] for s in solicitudes])
    
    # --- MÉTRICAS UNIVERSALES ---
    costo_promedio = np.mean(costos)
    costo_por_km = np.sum(costos) / np.sum(distancias)
    costo_por_kg = np.sum(costos) / np.sum(pesos)
    
    print(f"Costo Promedio por Entrega: ${costo_promedio:.2f}")
    print(f"Costo Promedio por Kilómetro: ${costo_por_km:.2f}/km")
    print(f"Costo Promedio por Kg Transportado: ${costo_por_kg:.2f}/kg")
    print("\nDesglose de Costos por Zona:")
    
    # --- (Costos por zona) ---
    zonas_unicas = np.unique(zonas)
    costo_total_zona = []
    
    for z in zonas_unicas:
        costos_z = costos[zonas == z]
        total = np.sum(costos_z)
        promedio = np.mean(costos_z)
        costo_total_zona.append(total)
        print(f"  · Zona {z}: Costo Promedio = ${promedio:.2f} | Costo Total = ${total:.2f}")

    # --- Gráfico de Barras por Zona ---
    plt.figure(figsize=(8, 5))
    plt.bar(zonas_unicas, costo_total_zona, color='#4CAF50')
    plt.title("Costo Total Operativo por Zona")
    plt.xlabel("Zona de Destino")
    plt.ylabel("Costo Total ($)")
    plt.savefig("grafico_1_costos_zona.png")
    plt.close()

    # --- Scatter Distancia vs Costo ---
    plt.figure(figsize=(8, 5))
    plt.scatter(distancias, costos, alpha=0.5, color='#00BCD4')
    plt.title("Relación entre Distancia del Viaje y Costo Operativo")
    plt.xlabel("Distancia (km)")
    plt.ylabel("Costo ($)")
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.savefig("grafico_1a_scatter_costos.png")
    plt.close()

    # --- Pie Chart de Depósitos ---
    depositos_unicos = np.unique(depositos)
    costos_depositos = []
    for d in depositos_unicos:
        costos_depositos.append(np.sum(costos[depositos == d]))

    plt.figure(figsize=(7, 7))
    colores = ['#FF9999', '#66B3FF', '#99FF99', '#FFCC99', '#D0A9F5']
    plt.pie(costos_depositos, labels=depositos_unicos, autopct='%1.1f%%', startangle=140, colors=colores)
    plt.title("Distribución de Costos Operativos por Depósito")
    plt.tight_layout()
    plt.savefig("grafico_1b_pie_depositos.png")
    plt.close()

def analizar_ventanas(solicitudes):
    print("\n--- ANÁLISIS DE CUMPLIMIENTO DE VENTANAS (COMPLETO) ---")
    
    # Preparamos los arrays de NumPy con toda la info necesaria
    cumple = np.array([s['cumple_ventana'] == 'True' for s in solicitudes])
    zonas = np.array([s['zona_destino'] for s in solicitudes])
    transportes = np.array([s['transporte'] for s in solicitudes])
    fechas = np.array([s['fecha'] for s in solicitudes])
    meses = np.array([f[:7] for f in fechas]) # Extrae YYYY-MM
    
    # 1. Cumplimiento Global
    tasa_global = np.mean(cumple) * 100
    print(f"Cumplimiento Global: {tasa_global:.2f}%\n")
    
    # 2. Cumplimiento por Zona
    print("Cumplimiento por Zona:")
    zonas_unicas = np.unique(zonas)
    tasa_por_zona = []
    for z in zonas_unicas:
        tasa = np.mean(cumple[zonas == z]) * 100
        tasa_por_zona.append(tasa)
        print(f"  · Zona {z}: {tasa:.2f}%")

    # 3. Cumplimiento por Tipo de Transporte (¡NUEVO!)
    print("\nCumplimiento por Tipo de Transporte:")
    tipos_unicos = np.unique(transportes)
    for t in tipos_unicos:
        tasa_transporte = np.mean(cumple[transportes == t]) * 100
        print(f"  · Vehículo '{t}': {tasa_transporte:.2f}%")
        
    # 4. Cumplimiento Mensual (¡NUEVO!)
    print("\nCumplimiento Mensual:")
    meses_ordenados = np.sort(np.unique(meses)) 
    tasas_mensuales = []
    for m in meses_ordenados:
        tasa_mes = np.mean(cumple[meses == m]) * 100
        tasas_mensuales.append(tasa_mes)
        print(f"  · Mes {m}: {tasa_mes:.2f}%")

    # --- GENERACIÓN DE GRÁFICOS ---
    
    # Gráfico A: Barras por Zona (El que ya tenías)
    plt.figure(figsize=(8, 5))
    plt.bar(zonas_unicas, tasa_por_zona, color='#2196F3')
    plt.title("Porcentaje de Cumplimiento de Ventanas por Zona")
    plt.ylabel("Cumplimiento (%)")
    plt.ylim(0, 100)
    plt.savefig("grafico_2_ventanas_zona.png")
    plt.close()

    # Gráfico B: Serie Temporal Mensual (El nuevo)
    plt.figure(figsize=(10, 5))
    plt.plot(meses_ordenados, tasas_mensuales, marker='o', color='#E91E63', linewidth=2, markersize=8)
    plt.title("Evolución Mensual: Cumplimiento de Ventanas Horarias")
    plt.xlabel("Mes del Año")
    plt.ylabel("Cumplimiento (%)")
    plt.ylim(0, 100)
    plt.xticks(rotation=45)
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.tight_layout()
    plt.savefig("grafico_6_serie_temporal_ventanas.png")
    plt.close()
    
def analizar_incidencias_completas(solicitudes, incidencias):
    print("\n--- ANÁLISIS DE INCIDENCIAS ---")
    
    # 1. Porcentaje de entregas con incidencias
    total_solicitudes = len(solicitudes)
    # Contamos cuántas solicitudes tienen el campo 'incidencias' mayor a 0
    sol_con_incidencias = np.sum(np.array([int(s['incidencias']) for s in solicitudes]) > 0)
    porcentaje_inc = (sol_con_incidencias / total_solicitudes) * 100
    print(f"Porcentaje de entregas con incidencias: {porcentaje_inc:.2f}% ({sol_con_incidencias} de {total_solicitudes} viajes)")

    # 2. Preparar el cruce de datos (JOIN) entre incidencias y solicitudes
    # Armamos un diccionario rápido para buscar la solicitud por su ID
    sol_dict = {s['id_solicitud']: s for s in solicitudes}
    
    tipos_inc = []
    zonas_inc = []
    trans_inc = []
    
    for inc in incidencias:
        id_sol = inc['id_solicitud']
        if id_sol in sol_dict: # Si encontramos la solicitud original
            sol = sol_dict[id_sol]
            tipos_inc.append(inc['tipo'])
            zonas_inc.append(sol['zona_destino'])
            trans_inc.append(sol['transporte'])
            
    # Convertimos a arrays de NumPy para cálculos rápidos
    tipos_inc = np.array(tipos_inc)
    zonas_inc = np.array(zonas_inc)
    trans_inc = np.array(trans_inc)
    
    # 3. Métricas desglosadas
    print("\nIncidencias por Tipo:")
    tipos_unicos, counts_tipos = np.unique(tipos_inc, return_counts=True)
    for t, c in zip(tipos_unicos, counts_tipos):
        print(f"  · {t}: {c}")
        
    print("\nIncidencias por Zona:")
    zonas_unicas, counts_zonas = np.unique(zonas_inc, return_counts=True)
    for z, c in zip(zonas_unicas, counts_zonas):
        print(f"  · {z}: {c}")
        
    print("\nIncidencias por Transporte:")
    trans_unicos, counts_trans = np.unique(trans_inc, return_counts=True)
    for tr, c in zip(trans_unicos, counts_trans):
        print(f"  · {tr}: {c}")

    # --- GENERACIÓN DE GRÁFICOS ---
    
    # Gráfico A: Piechart de incidencias por zona
    plt.figure(figsize=(7, 7))
    colores_pie = ['#FF9999', '#66B3FF', '#99FF99', '#FFCC99', '#D0A9F5']
    plt.pie(counts_zonas, labels=zonas_unicas, autopct='%1.1f%%', startangle=90, colors=colores_pie)
    plt.title("Distribución de Incidencias por Zona")
    plt.tight_layout()
    plt.savefig("grafico_incidencias_1_pie_zona.png")
    plt.close()
    
    # Gráfico B: Barras apiladas (Transporte vs Tipo de incidencia)
    # Matriz para contar cruces
    matriz_trans_tipo = np.zeros((len(trans_unicos), len(tipos_unicos)))
    for i, tr in enumerate(trans_unicos):
        for j, t in enumerate(tipos_unicos):
            matriz_trans_tipo[i, j] = np.sum((trans_inc == tr) & (tipos_inc == t))
    
    plt.figure(figsize=(9, 6))
    bottoms = np.zeros(len(trans_unicos))
    colores_barras = ['#F44336', '#FFC107', '#2196F3', '#4CAF50'] # Rojo, Amarillo, Azul
    
    for j, t in enumerate(tipos_unicos):
        plt.bar(trans_unicos, matriz_trans_tipo[:, j], bottom=bottoms, label=t, color=colores_barras[j % len(colores_barras)])
        bottoms += matriz_trans_tipo[:, j] # Subimos la base para apilar la siguiente barra
        
    plt.title("Tipos de Incidencias por Tipo de Transporte")
    plt.ylabel("Cantidad de Incidencias")
    plt.legend(title="Tipo de Incidencia")
    plt.grid(axis='y', linestyle='--', alpha=0.5)
    plt.tight_layout()
    plt.savefig("grafico_incidencias_2_barras_transporte.png")
    plt.close()
    
    # Gráfico C: Heatmap (Zona vs Tipo de incidencia)
    matriz_zona_tipo = np.zeros((len(zonas_unicas), len(tipos_unicos)))
    for i, z in enumerate(zonas_unicas):
        for j, t in enumerate(tipos_unicos):
            matriz_zona_tipo[i, j] = np.sum((zonas_inc == z) & (tipos_inc == t))
            
    plt.figure(figsize=(8, 6))
    plt.imshow(matriz_zona_tipo, cmap='Reds', aspect='auto') # Usamos un mapa de calor rojo
    plt.colorbar(label='Frecuencia de Incidencias')
    plt.xticks(np.arange(len(tipos_unicos)), tipos_unicos)
    plt.yticks(np.arange(len(zonas_unicas)), zonas_unicas)
    plt.title("Heatmap: Zona de Destino vs Tipo de Incidencia")
    
    # Escribimos los números adentro de los cuadraditos del heatmap
    for i in range(len(zonas_unicas)):
        for j in range(len(tipos_unicos)):
            plt.text(j, i, int(matriz_zona_tipo[i, j]), ha='center', va='center', color='black', fontweight='bold')
            
    plt.tight_layout()
    plt.savefig("grafico_incidencias_3_heatmap_zona.png")
    plt.close()
    
def analizar_utilizacion_flota(solicitudes):
    print("\n--- ANÁLISIS DE UTILIZACIÓN DE FLOTA (PESOS) ---")
    transportes = np.array([s['transporte'] for s in solicitudes])
    pesos = np.array([float(s['peso_kg']) for s in solicitudes])
    
    tipos_unicos = np.unique(transportes)
    datos_boxplot = []
    
    for t in tipos_unicos:
        pesos_t = pesos[transportes == t]
        datos_boxplot.append(pesos_t)
        print(f"Vehículo '{t}': Peso Promedio transportado = {np.mean(pesos_t):.2f} kg")

    plt.figure(figsize=(8, 5))
    plt.boxplot(datos_boxplot, tick_labels=tipos_unicos, patch_artist=True)
    plt.title("Distribución de Pesos Transportados por Vehículo (Boxplot)")
    plt.ylabel("Peso (kg)")
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.savefig("grafico_3_utilizacion.png")
    plt.close()

def analizar_entregas_y_volumen(solicitudes):
    print("\n--- ANÁLISIS DE ENTREGAS REALIZADAS Y VOLUMEN PROMEDIO ---")
    transportes_sol = np.array([s['transporte'] for s in solicitudes])
    volumenes_sol = np.array([float(s['volumen_m3']) for s in solicitudes])
    
    # Filtramos para contar SOLO las entregas que se realizaron con éxito
    entregas_exitosas = np.array([s['entregada'] == 'True' for s in solicitudes])

    tipos_vehiculos = ["Moto", "Furgoneta", "Camión"]
    cantidades = []
    volumenes_promedio = []

    for t in tipos_vehiculos:
        filtro_vehiculo = (transportes_sol == t)
        
        # Combinamos filtros: que sea de este vehículo Y que se haya entregado
        cant_entregas = np.sum(filtro_vehiculo & entregas_exitosas)
        vol_promedio = np.mean(volumenes_sol[filtro_vehiculo])
        
        cantidades.append(cant_entregas)
        volumenes_promedio.append(vol_promedio)
        
        print(f"Vehículo '{t}':")
        print(f"  · Entregas exitosas realizadas: {cant_entregas}")
        print(f"  · Volumen promedio transportado: {vol_promedio:.2f} m³\n")

    # Gráfico de doble eje (Barras + Línea)
    fig, ax1 = plt.subplots(figsize=(8, 5))

    # Eje 1 (Izquierdo) - Cantidad de Entregas (Barras)
    color1 = '#9C27B0' # Violeta
    ax1.set_xlabel('Tipo de Vehículo')
    ax1.set_ylabel('Cantidad de Entregas Exitosas', color=color1)
    barras = ax1.bar(tipos_vehiculos, cantidades, color=color1, alpha=0.7, width=0.5, label='Entregas')
    ax1.tick_params(axis='y', labelcolor=color1)
    
    # Etiquetas en las barras
    for barra in barras:
        yval = barra.get_height()
        ax1.text(barra.get_x() + barra.get_width()/2, yval + 5, f"{int(yval)}", ha='center', va='bottom', fontweight='bold', color='black')

    # Eje 2 (Derecho) - Volumen Promedio (Línea)
    ax2 = ax1.twinx()  
    color2 = '#FF5722' # Naranja oscuro
    ax2.set_ylabel('Volumen Promedio (m³)', color=color2)  
    ax2.plot(tipos_vehiculos, volumenes_promedio, color=color2, marker='o', linestyle='dashed', linewidth=2, markersize=8, label='Volumen Promedio')
    ax2.tick_params(axis='y', labelcolor=color2)
    
    # Ajustamos la escala del eje Y derecho para que la línea no se solape con las barras
    ax2.set_ylim(0, max(volumenes_promedio) * 1.3)

    # Etiquetas en los puntos de la línea
    for i, txt in enumerate(volumenes_promedio):
        ax2.annotate(f"{txt:.2f} m³", (tipos_vehiculos[i], volumenes_promedio[i]), 
                     textcoords="offset points", xytext=(0,10), ha='center', fontweight='bold', color=color2)

    plt.title("Relación: Entregas Realizadas vs Volumen Promedio")
    fig.tight_layout()  
    plt.savefig("grafico_5_entregas_y_volumen.png")
    plt.close()
    print("✓ Gráfico combinado guardado como 'grafico_5_entregas_y_volumen.png'")

def analizar_impacto_ambiental_completo(solicitudes):
    print("\n--- ANÁLISIS DE IMPACTO AMBIENTAL ---")
    
    # 1. Preparar arrays de NumPy (el impacto ambiental ya equivale a distancia * emisión)
    impactos = np.array([float(s['impacto_ambiental']) for s in solicitudes])
    transportes = np.array([s['transporte'] for s in solicitudes])
    pesos = np.array([float(s['peso_kg']) for s in solicitudes])
    zonas = np.array([s['zona_destino'] for s in solicitudes])
    fechas = np.array([s['fecha'] for s in solicitudes])
    meses = np.array([f[:7] for f in fechas])
    
    # 2. Cálculos y Métricas
    emision_total = np.sum(impactos)
    peso_total = np.sum(pesos)
    emision_por_kg = emision_total / peso_total
    
    print(f"Emisiones Totales Generadas: {emision_total:.2f} kg CO2")
    print(f"Emisiones por Kg Transportado: {emision_por_kg:.4f} kg CO2 por cada kg")
    
    print("\nEmisiones por Tipo de Vehículo:")
    tipos_unicos = np.unique(transportes)
    emisiones_por_tipo = []
    for t in tipos_unicos:
        emision_t = np.sum(impactos[transportes == t])
        emisiones_por_tipo.append(emision_t)
        print(f"  · {t}: {emision_t:.2f} kg CO2")
        
    print("\nEmisiones por Zona de Destino:")
    zonas_unicas = np.unique(zonas)
    for z in zonas_unicas:
        emision_z = np.sum(impactos[zonas == z])
        print(f"  · Zona {z}: {emision_z:.2f} kg CO2")

    # --- GENERACIÓN DE GRÁFICOS ---
    meses_unicos = np.sort(np.unique(meses))
    
    # Preparamos los datos mensuales
    matriz_mes_tipo = np.zeros((len(meses_unicos), len(tipos_unicos)))
    emisiones_mensuales = np.zeros(len(meses_unicos))
    
    for i, m in enumerate(meses_unicos):
        filtro_mes = (meses == m)
        emisiones_mensuales[i] = np.sum(impactos[filtro_mes])
        for j, t in enumerate(tipos_unicos):
            matriz_mes_tipo[i, j] = np.sum(impactos[filtro_mes & (transportes == t)])

    # Gráfico A: Barras comparativas de emisiones por tipo de vehículo por mes
    plt.figure(figsize=(12, 6))
    x = np.arange(len(meses_unicos))
    ancho = 0.25 # Ancho de cada barrita
    
    colores_vehiculos = ['#F44336', '#2196F3', '#FFEB3B'] # Colores fijos para distinguir
    for j, t in enumerate(tipos_unicos):
        # Desfasamos las barras para que queden agrupadas y no superpuestas
        offset = (j - 1) * ancho if len(tipos_unicos) == 3 else j * ancho
        plt.bar(x + offset, matriz_mes_tipo[:, j], ancho, label=t, color=colores_vehiculos[j])
        
    plt.title("Emisiones Comparativas por Tipo de Vehículo Mensualmente")
    plt.xlabel("Mes")
    plt.ylabel("Emisiones (kg CO2)")
    plt.xticks(x, meses_unicos, rotation=45)
    plt.legend()
    plt.grid(axis='y', linestyle='--', alpha=0.5)
    plt.tight_layout()
    plt.savefig("grafico_ambiental_1_comparativo_mes.png")
    plt.close()
    
    # Gráfico B: Acumulado de emisiones mensual en gráfico de barras
    plt.figure(figsize=(10, 5))
    emisiones_acumuladas = np.cumsum(emisiones_mensuales) # Va sumando el total histórico
    
    plt.bar(meses_unicos, emisiones_acumuladas, color='#4CAF50', alpha=0.8)
    plt.title("Crecimiento Acumulado de Emisiones a lo largo del Año")
    plt.xlabel("Mes")
    plt.ylabel("Emisiones Acumuladas (kg CO2)")
    plt.xticks(rotation=45)
    
    # Escribimos el valor total arriba de cada barra
    for i, valor in enumerate(emisiones_acumuladas):
        plt.text(i, valor + (max(emisiones_acumuladas)*0.01), f"{int(valor)}", ha='center', va='bottom', fontsize=8)

    plt.grid(axis='y', linestyle='--', alpha=0.5)
    plt.tight_layout()
    plt.savefig("grafico_ambiental_2_acumulado_mensual.png")
    plt.close()

    # Gráfico C: Participación % de emisiones por tipo de vehículo
    plt.figure(figsize=(7, 7))
    colores_pie = ['#FF9800', '#03A9F4', '#9C27B0']
    plt.pie(emisiones_por_tipo, labels=tipos_unicos, autopct='%1.1f%%', startangle=140, colors=colores_pie)
    plt.title("Participación % de Emisiones por Tipo de Vehículo")
    plt.tight_layout()
    plt.savefig("grafico_ambiental_3_pie_vehiculos.png")
    plt.close()
def calcular_utilizacion_capacidad(solicitudes, vehiculos):
    print("\n--- ANÁLISIS DE UTILIZACIÓN DE CAPACIDAD (PESO Y VOLUMEN) ---")
    tipos_vehiculos = ["Moto", "Furgoneta", "Camión"]
    
    # 1. Arrays de Solicitudes
    transportes_sol = np.array([s['transporte'] for s in solicitudes])
    pesos_sol = np.array([float(s['peso_kg']) for s in solicitudes])
    volumenes_sol = np.array([float(s['volumen_m3']) for s in solicitudes])
    
    # 2. Arrays de Vehículos
    tipos_veh = np.array([v['tipo'] for v in vehiculos])
    cap_peso_veh = np.array([float(v['capacidad_max_kg']) for v in vehiculos])
    cap_vol_veh = np.array([float(v['capacidad_max_m3']) for v in vehiculos])
    
    utilizacion_peso = []
    utilizacion_volumen = []
    
    # 3. Cálculos
    for t in tipos_vehiculos:
        # Medias de capacidad
        media_cap_peso = np.mean(cap_peso_veh[tipos_veh == t])
        media_cap_vol = np.mean(cap_vol_veh[tipos_veh == t])
        
        # Medias transportadas
        media_peso_trans = np.mean(pesos_sol[transportes_sol == t])
        media_vol_trans = np.mean(volumenes_sol[transportes_sol == t])
        
        # Porcentajes
        porc_peso = (media_peso_trans / media_cap_peso) * 100
        porc_vol = (media_vol_trans / media_cap_vol) * 100
        
        utilizacion_peso.append(porc_peso)
        utilizacion_volumen.append(porc_vol)
        
        print(f"Vehículo '{t}':")
        print(f"  · Peso: Utilización del {porc_peso:.2f}% (Media trans: {media_peso_trans:.2f} kg / Cap: {media_cap_peso:.2f} kg)")
        print(f"  · Volumen: Utilización del {porc_vol:.2f}% (Media trans: {media_vol_trans:.2f} m3 / Cap: {media_cap_vol:.2f} m3)\n")

    # 4. Gráfico de barras agrupadas
    x = np.arange(len(tipos_vehiculos))  # Posiciones para las etiquetas
    ancho = 0.35  # Ancho de las barras

    plt.figure(figsize=(9, 6))
    barras_peso = plt.bar(x - ancho/2, utilizacion_peso, ancho, label='Utilización Peso (%)', color='#2196F3')
    barras_vol = plt.bar(x + ancho/2, utilizacion_volumen, ancho, label='Utilización Volumen (%)', color='#FF9800')

    plt.title("Porcentaje de Utilización de Capacidad (Peso vs Volumen)")
    plt.ylabel("Utilización (%)")
    plt.xticks(x, tipos_vehiculos)
    
    # Marcador de límite 100%
    plt.axhline(y=100, color='red', linestyle='--', alpha=0.7, label="Capacidad Máxima (100%)")
    plt.legend()

    # Agregar etiquetas arriba de las barras
    for barra in barras_peso + barras_vol:
        yval = barra.get_height()
        plt.text(barra.get_x() + barra.get_width()/2, yval + 1, f"{yval:.1f}%", ha='center', va='bottom', fontsize=8, fontweight='bold')

    plt.grid(axis='y', linestyle='--', alpha=0.3)
    plt.tight_layout()
    plt.savefig("grafico_4_utilizacion_capacidad.png")
    plt.close()    

def simular_mejora_ambiental(solicitudes):
    print("\n--- SIMULACIÓN AMBIENTAL (ESCENARIO DE MEJORA) ---")
    transportes = np.array([s['transporte'] for s in solicitudes])
    distancias = np.array([float(s['distancia_km']) for s in solicitudes])
    impactos = np.array([float(s['impacto_ambiental']) for s in solicitudes])
    
    impacto_actual = np.sum(impactos)
    
    # Análisis del escenario: 20% de la distancia de Camiones pasa a Furgonetas
    filtro_camion = (transportes == 'Camión')
    distancia_camion = np.sum(distancias[filtro_camion])
    impacto_camion_actual = distancia_camion * 0.80
    
    distancia_migrada = distancia_camion * 0.20
    # El impacto recalculado suma el 80% restante en camión más el 20% con factor de furgoneta
    nuevo_impacto_camion = (distancia_camion * 0.80) - (distancia_migrada * 0.80) + (distancia_migrada * 0.35)
    
    impacto_simulado = impacto_actual - impacto_camion_actual + nuevo_impacto_camion
    ahorro = impacto_actual - impacto_simulado
    porcentaje_reduccion = (ahorro / impacto_actual) * 100
    
    print(f"Impacto Ambiental Actual de la Flota: {impacto_actual:.2f} kg CO2")
    print(f"Impacto Simulado (20% Camiones -> Furgonetas): {impacto_simulado:.2f} kg CO2")
    print(f"Resultado: Ahorro Total de {ahorro:.2f} kg CO2 ({porcentaje_reduccion:.2f}% de reducción general)")


def main():
    print("Iniciando análisis avanzado de LISASA...")
    solicitudes, incidencias, vehiculos = cargar_datos()
    
    analizar_costos_por_zona(solicitudes)
    analizar_entregas_y_volumen(solicitudes)
    analizar_ventanas(solicitudes)
    analizar_incidencias_completas(solicitudes, incidencias)
    analizar_impacto_ambiental_completo(solicitudes)
    analizar_utilizacion_flota(solicitudes)
    simular_mejora_ambiental(solicitudes)
    calcular_utilizacion_capacidad(solicitudes, vehiculos)


if __name__ == "__main__":
    main()