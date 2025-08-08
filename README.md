# Proyecto de Predicción de Churn

Este proyecto tiene como objetivo predecir la cancelación de clientes para una empresa de telecomunicaciones. Abarca varias etapas de un proyecto de ciencia de datos, desde la ingeniería y el análisis de datos hasta el aprendizaje automático.

## Estructura del Proyecto

.
├── data/
│   └── raw/
│       └── telco_churn.csv
├── output/
│   └── data_report.html
├── scripts/
│   └── data_summary.py
├── .gitignore
├── README.md
└── requirements.txt


## Configuración

1.  **Clona el repositorio:**
    ```bash
    git clone <repository-url>
    cd churn_prediction_project
    ```

2.  **Instala las dependencias:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Credenciales de la API de Kaggle:**
    Para descargar los datos, necesitas tener tus credenciales de la API de Kaggle configuradas. Coloca tu archivo `kaggle.json` en `~/.kaggle/`.

## Uso

### Paso 1: Descargar los Datos

Este paso descarga el conjunto de datos "Telco Customer Churn" de Kaggle.

```bash
python scripts/data_summary.py --download
```

Esto guardará el archivo `telco_churn.csv` en el directorio `data/raw/`.

### Paso 2: Generar el Resumen de Datos (Completado)

Este paso genera un informe detallado del perfil de los datos usando `ydata-profiling` y lo guarda como un archivo HTML. Este informe ayuda a comprender la distribución de los datos, los valores faltantes y otras características importantes del conjunto de datos.

```bash
python scripts/data_summary.py
```

El informe se guardará como `output/data_report.html`.

### Paso 3: Análisis Exploratorio de Datos (EDA)

Se ha realizado un análisis exploratorio inicial en el notebook `notebooks/01_basic_data_exploration.ipynb`. Este cuaderno cubre los siguientes pasos:

- Carga de datos con Pandas.
- Inspección inicial de los datos (`head`, `info`).
- Identificación y manejo de valores nulos en `TotalCharges`.
- Cálculo de estadísticas descriptivas.
- Visualización de la distribución de `MonthlyCharges` (histograma) y la frecuencia de `Churn` (gráfico de barras).