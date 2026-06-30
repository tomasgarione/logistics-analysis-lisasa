import csv
import numpy as np
from datetime import datetime, timedelta

def generar_datasets():
    print("Iniciando generación de datos sintéticos con límites exactos del TP...")
    
    # --- 1. GENERAR VEHÍCULOS (CON CAPACIDADES EXACTAS DEL CÓDIGO) ---
    tipos_vehiculos = ["Moto", "Furgoneta", "Camión"]
    estados = ["Disponible", "En mantenimiento", "En ruta"]
    vehiculos = []
    
    for i in range(1, 51):
        tipo = np.random.choice(tipos_vehiculos, p=[0.4, 0.4, 0.2])
        
        # Asignación de capacidades 
        if tipo == "Moto":
            cap_peso = 100.0    
            cap_vol = 0.5       
            emision = 0.10
        elif tipo == "Furgoneta":
            cap_peso = 500.0    
            cap_vol = 10.0 
            emision = 0.35     
        else: # Camión
            cap_peso = 5000.0   
            cap_vol = 30.0      
            emision = 0.80
            
        estado = np.random.choice(estados, p=[0.7, 0.1, 0.2])
        vehiculos.append([i, f"LIS-{i:03d}", tipo, cap_peso, cap_vol, emision, estado])
        
    with open("dataset_vehiculos.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["id_vehiculo", "patente", "tipo", "capacidad_max_kg", "capacidad_max_m3", "factor_emision", "estado"])
        writer.writerows(vehiculos)

    # --- 2. GENERAR SOLICITUDES E INCIDENCIAS ---
    depositos = ["D1", "D2", "D3", "D4", "D5"]
    zonas = ["Centro", "Norte", "Sur", "Este", "Oeste"]
    costos_base = {"Moto": 80.0, "Furgoneta": 120.0, "Camión": 200.0}
    
    solicitudes = []
    incidencias = []
    fecha_base = datetime.now() - timedelta(days=365)
    id_incidencia = 1
    
    for i in range(1, 1001):
        dias_random = np.random.randint(0, 365)
        fecha = (fecha_base + timedelta(days=dias_random)).strftime("%Y-%m-%d")
        
        deposito = np.random.choice(depositos)
        zona = np.random.choice(zonas)
        
        # Determinamos el tipo de transporte primero para generar peso/volumen coherentes
        transporte = np.random.choice(tipos_vehiculos, p=[0.45, 0.40, 0.15])
        
        # Generamos peso y volumen DENTRO de los límites del código original
        if transporte == "Moto":
            peso = round(np.random.uniform(0.5, 100.0), 2)
            volumen = round(np.random.uniform(0.01, 0.5), 2)
        elif transporte == "Furgoneta":
            peso = round(np.random.uniform(20.0, 500.0), 2)
            volumen = round(np.random.uniform(0.5, 10.0), 2)
        else: # Camión
            peso = round(np.random.uniform(100.0, 5000.0), 2)
            volumen = round(np.random.uniform(5.0, 30.0), 2)
            
        distancia = round(np.random.uniform(1, 60), 2)
        
        hora_inicio = np.random.randint(8, 16)
        hora_fin = hora_inicio + np.random.randint(1, 5)
        
        # 1. Forzamos la probabilidad: 90% True, 10% False
        cumple_ventana = np.random.choice([True, False], p=[0.90, 0.10])
        
        # 2. Asignamos la hora coherente con el resultado anterior
        if cumple_ventana:
            hora_prevista = round(np.random.uniform(hora_inicio, hora_fin), 1)
        else:
            hora_prevista = round(np.random.uniform(hora_fin + 0.1, hora_fin + 2.0), 1)
        
        entregada = np.random.choice([True, False], p=[0.90, 0.10])
        
        cantidad_paradas = np.random.randint(1, 6)
        costo_viaje = round((distancia * costos_base[transporte]) + (500 * cantidad_paradas), 2)
        
        factor_emision = 0.10 if transporte == "Moto" else (0.35 if transporte == "Furgoneta" else 0.80)
        impacto_ambiental = round(distancia * factor_emision, 2)
        
        # El 85% de los viajes no tiene problemas, el 13% tiene 1, el 2% tiene 2
        cant_incidencias = np.random.choice([0, 1, 2], p=[0.85, 0.13, 0.02])
        
        for _ in range(cant_incidencias):
            tipo_incidencia = np.random.choice(["RETRASO", "AUSENTE", "DAÑO"], p=[0.60, 0.25, 0.15])
            gravedad = np.random.randint(1, 6)
            minutos = np.random.randint(10, 180) if tipo_incidencia == "RETRASO" else 0
            incidencias.append([id_incidencia, i, tipo_incidencia, gravedad, minutos])
            id_incidencia += 1
            
        solicitudes.append([i, fecha, deposito, zona, transporte, peso, volumen, distancia, 
                            cantidad_paradas, hora_inicio, hora_fin, hora_prevista, cumple_ventana, 
                            entregada, costo_viaje, impacto_ambiental, cant_incidencias])

    with open("dataset_solicitudes.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["id_solicitud", "fecha", "deposito_origen", "zona_destino", "transporte", 
                         "peso_kg", "volumen_m3", "distancia_km", "cantidad_paradas", "hora_inicio_ventana", 
                         "hora_fin_ventana", "hora_prevista", "cumple_ventana", "entregada", "costo_viaje", 
                         "impacto_ambiental", "incidencias"])
        writer.writerows(solicitudes)

    with open("dataset_incidencias.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["id_incidencia", "id_solicitud", "tipo", "gravedad", "minutos_retraso"])
        writer.writerows(incidencias)

    print("✓ Se generaron los 3 archivos CSV con las lógicas y capacidades estrictas de tu TP.")

if __name__ == "__main__":
    generar_datasets()