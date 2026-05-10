"""
Generador de Datos de Sensores IoT - Equipos Petroleros
Simula lecturas de temperatura, vibración, presión y acústica
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta

np.random.seed(42)

def generar_lecturas_sensor(equipo_id, tipo_equipo, num_dias=180):
    """Genera datos de sensores para un equipo"""

    datos = []
    fecha_inicio = datetime(2024, 1, 1)

    # Parámetros base según tipo de equipo
    if tipo_equipo == 'Compresor':
        temp_normal = np.random.uniform(75, 85)
        vibr_normal = np.random.uniform(2, 4)
        prob_anomalia = 0.08
    elif tipo_equipo == 'Bomba':
        temp_normal = np.random.uniform(65, 75)
        vibr_normal = np.random.uniform(1.5, 3)
        prob_anomalia = 0.12
    else:  # Turbina
        temp_normal = np.random.uniform(80, 95)
        vibr_normal = np.random.uniform(3, 5)
        prob_anomalia = 0.10

    for dia in range(num_dias):
        # 24 lecturas por día (cada hora)
        for hora in range(24):
            timestamp = fecha_inicio + timedelta(days=dia, hours=hora)

            # Simular anomalías
            es_anomalia = np.random.random() < prob_anomalia

            if es_anomalia:
                # Anomalía: valores fuera de rango
                temperatura = temp_normal + np.random.uniform(15, 35)
                vibracion = vibr_normal + np.random.uniform(2, 5)
                presion = np.random.uniform(50, 70)  # Baja
                ruido_db = np.random.uniform(95, 110)  # Alto
                etiqueta = np.random.choice(['fuga', 'sobrecalentamiento', 'desgaste'])
            else:
                # Normal: variación pequeña
                temperatura = temp_normal + np.random.uniform(-5, 5)
                vibracion = vibr_normal + np.random.uniform(-0.5, 0.5)
                presion = np.random.uniform(85, 115)  # Normal
                ruido_db = np.random.uniform(65, 85)  # Normal
                etiqueta = 'normal'

            datos.append({
                'equipo_id': equipo_id,
                'timestamp': timestamp,
                'tipo_equipo': tipo_equipo,
                'temperatura_c': max(0, temperatura),
                'vibracion_mm_s': max(0, vibracion),
                'presion_psi': max(0, presion),
                'ruido_db': ruido_db,
                'etiqueta': etiqueta
            })

    return datos

# Generar dataset
print("Generando datos de sensores IoT...")

equipos = (
    [('COMP-' + str(i).zfill(3), 'Compresor') for i in range(1, 21)] +
    [('PUMP-' + str(i).zfill(3), 'Bomba') for i in range(1, 26)] +
    [('TURB-' + str(i).zfill(3), 'Turbina') for i in range(1, 16)]
)

todos_datos = []
for equipo_id, tipo in equipos:
    datos = generar_lecturas_sensor(equipo_id, tipo, num_dias=180)
    todos_datos.extend(datos)
    if len(todos_datos) % 50000 == 0:
        print(f"  - Generados {len(todos_datos):,} registros...")

df = pd.DataFrame(todos_datos)

# Features adicionales
df['hora'] = df['timestamp'].dt.hour
df['dia_semana'] = df['timestamp'].dt.dayofweek
df['es_anomalia'] = (df['etiqueta'] != 'normal').astype(int)

# Guardar
df.to_csv('data/sensores_iot.csv', index=False)

print(f"\n[OK] Dataset generado!")
print(f"   Total registros: {len(df):,}")
print(f"   Total equipos: {df['equipo_id'].nunique()}")
print(f"   Periodo: {df['timestamp'].min()} a {df['timestamp'].max()}")
print(f"\nDistribucion de anomalias:")
print(df['etiqueta'].value_counts())
print(f"\nPorcentaje anomalias: {df['es_anomalia'].mean()*100:.2f}%")
