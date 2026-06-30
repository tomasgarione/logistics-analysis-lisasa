## Logistics Analysis & Cost Optimization – LISASA
# Descripción

Este proyecto consiste en el desarrollo de un sistema para el análisis de operaciones logísticas, enfocado en la detección de incidencias críticas y la evaluación de costos operativos.

El objetivo es mejorar la visibilidad sobre fallas en entregas y permitir la simulación de ajustes de costos en función de variables económicas.

# Objetivos
* Identificar incidencias críticas en entregas (ej: productos dañados)
* Generar reportes automatizados para análisis operativo
* Simular ajustes de costos operativos (inflación)
* Modelar estructuras de datos representando operaciones logísticas

# Funcionalidades
# Detección de Incidencias

A partir de un conjunto de entregas:
* Filtra aquellas con fallas críticas
* Extrae descripciones relevantes
* Genera un archivo .csv con los resultados

# Ajuste de Costos
* Aplica un incremento del 15% sobre costos operativos base
* Permite simular impacto de inflación en distintos tipos de transporte

# Estructura del Proyecto
└── src/<br>
│   ├── entregas.py<br>
│   ├── transporte.py<br>
│   └── analisis.py<br>
└──  tests/<br>
│   └── test_analisis.py<br>
└──  data/<br>
│   └── entregas.csv<br>
└──  README.md<br>

# Tecnologías utilizadas
* Python
* pandas
* pytest
* CSV processing

# Testing
El proyecto incluye tests automatizados utilizando pytest para validar:
* Correcta detección de incidencias críticas
* Aplicación adecuada de ajustes de costos
* Consistencia en los resultados generados

Para correr los tests:
pytest

# Ejecución
Clonar el repositorio:<br>
git clone https://github.com/TUUSUARIO/TUREPO.git<br>
cd TUREPO

Ejecutar el script principal:
python src/analisis.py

# Ejemplo de Output
Archivo generado:

incidencias_criticas.csv

Contenido:

DAÑO EN PRODUCTO
ROTURA DURANTE TRANSPORTE
FALLA CRÍTICA EN ENTREGA

# Contexto Académico
Proyecto desarrollado como parte de la cursada en el ITBA (Instituto Tecnológico de Buenos Aires), enfocado en la aplicación de programación y análisis de datos a problemas logísticos.

# Posibles mejoras
* Integración con bases de datos (SQL)
* Visualización de métricas en dashboards
* Análisis exploratorio de datos (EDA)
* Modelos predictivos para incidencias
