import os
import pandas as pd
import numpy as np
from datetime import datetime
import argparse
import zipfile

def download_dataset():
    """
    Intenta descargar el dataset de Telco Customer Churn desde Kaggle usando la API.
    Requiere que exista el archivo ~/.kaggle/kaggle.json con el token válido.
    """
    try:
        from kaggle.api.kaggle_api_extended import KaggleApi
    except ImportError:
        print("Error: la librería 'kaggle' no está instalada. Ejecuta: pip install kaggle")
        return False

    # Verificar que el archivo de credenciales existe
    home = os.path.expanduser("~")
    kaggle_json_path = os.path.join(home, ".kaggle", "kaggle.json")
    if not os.path.isfile(kaggle_json_path):
        print(f"No se encontró el archivo de credenciales en {kaggle_json_path}.")
        print("Descarga tu API token desde Kaggle y colócalo ahí.")
        return False

    try:
        api = KaggleApi()
        api.authenticate()
        
        dataset_id = "blastchar/telco-customer-churn"
        file_name = "WA_Fn-UseC_-Telco-Customer-Churn.csv"
        download_path = os.path.join("data", "raw")
        final_csv_path = os.path.join(download_path, "telco_churn.csv")

        os.makedirs(download_path, exist_ok=True)

        print(f"Descargando {file_name} de {dataset_id} a {download_path}...")
        api.dataset_download_file(dataset_id, file_name, path=download_path)
        
        zip_path = os.path.join(download_path, f"{file_name}.zip")
        if os.path.isfile(zip_path):
            print("Descomprimiendo archivo...")
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(download_path)
            os.remove(zip_path)
            # Renombrar el archivo extraído al nombre final esperado
            os.rename(os.path.join(download_path, file_name), final_csv_path)

        print(f"Descarga completada. Archivo guardado en: {final_csv_path}")
        return True
    except Exception as e:
        print(f"Falló la descarga automática desde Kaggle: {e}")
        return False

def summarize_data(csv_path, output_html):
    """
    Genera un reporte de perfil de datos y lo guarda como un archivo HTML.
    """
    try:
        from ydata_profiling import ProfileReport
        
        print(f"Leyendo el archivo de datos desde {csv_path}...")
        df = pd.read_csv(csv_path)

        print("Generando el reporte de perfil de datos. Esto puede tardar unos segundos...")
        profile = ProfileReport(df, title="Reporte de Análisis de Churn de Clientes")

        print(f"Guardando el reporte en {output_html}...")
        profile.to_file(output_html)
        print(f"¡Reporte generado con éxito en {output_html}!")

    except FileNotFoundError:
        print(f"Error: No se encontró el archivo en la ruta: {csv_path}")
        print("Asegúrate de haber descargado los datos primero con la opción --download.")
    except Exception as e:
        print(f"Ocurrió un error inesperado al generar el reporte: {e}")

def count_rows(csv_path):
    """
    Lee un CSV y cuenta el número de filas y columnas.
    """
    try:
        df = pd.read_csv(csv_path)
        rows, cols = df.shape
        print(f"El archivo {os.path.basename(csv_path)} tiene {rows} filas y {cols} columnas.")
    except FileNotFoundError:
        print(f"Error: No se encontró el archivo en la ruta: {csv_path}")
    except Exception as e:
        print(f"Ocurrió un error inesperado: {e}")

def main():
    parser = argparse.ArgumentParser(description="Resumen básico de dataset de churn.")
    parser.add_argument('csv_path', nargs='?', default='data/raw/telco_churn.csv', help="Ruta al CSV")
    parser.add_argument('--download', action='store_true', help="Descargar el dataset desde Kaggle")
    parser.add_argument('--html', type=str, default='output/data_report.html', help="Ruta de salida del HTML")
    parser.add_argument('--count', action='store_true', help="Solo contar filas y columnas")
    args = parser.parse_args()

    if args.download:
        success = download_dataset()
        if not success:
            print("La descarga falló. Abortando.")
            return

    # Crear la carpeta de salida si no existe
    output_dir = os.path.dirname(args.html)
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)

    if args.count:
        count_rows(args.csv_path)
    else:
        summarize_data(args.csv_path, output_html=args.html)

if __name__ == "__main__":
    main()
