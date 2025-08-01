import os
import pandas as pd
import numpy as np
from datetime import datetime
import argparse

# Esto viene de la librería kaggle; solo funciona si pip install kaggle ya se hizo
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
        print("Descarga tu API token desde Kaggle y colócalo ahí. Ejemplo:")
        print("  1. Ve a tu cuenta en Kaggle > API > Create New API Token")
        print("  2. Mueve el kaggle.json a ~/.kaggle/ y dale permisos: chmod 600 ~/.kaggle/kaggle.json")
        return False

    try:
        api = KaggleApi()
        api.authenticate()
        # Descarga específica del CSV y lo descomprime en data/raw
        os.makedirs("data/raw", exist_ok=True)
        api.dataset_download_file(
            "blastchar/telco-customer-churn",
            "WA_Fn-UseC_-Telco-Customer-Churn.csv",
            path="data/raw"
        )
        # El archivo se descarga como un zip, necesitamos descomprimirlo
        import zipfile
        zip_path = os.path.join("data", "raw", "WA_Fn-UseC_-Telco-Customer-Churn.csv.zip")
        if os.path.isfile(zip_path):
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(os.path.join("data", "raw"))
            os.remove(zip_path)
        # Renombrar si el nombre no coincide con lo que esperas
        expected = os.path.join("data", "raw", "WA_Fn-UseC_-Telco-Customer-Churn.csv")
        target = os.path.join("data", "raw", "telco_churn.csv")
        if os.path.isfile(expected) and not os.path.isfile(target):
            os.replace(expected, target)
        print("Descarga automática completada y colocada en data/raw/telco_churn.csv")
        return True
    except Exception as e:
        print("Falló la descarga automática desde Kaggle:", str(e))
        print("Puedes descargar el archivo manualmente desde Kaggle y ponerlo en data/raw/telco_churn.csv")
        return False

def summarize_data(csv_path, output_html):
    pass

def count_rows(csv_path):
    pass

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
            # si falló, no abortamos forzosamente pero avisamos
            print("Continuando, pero revisa que el archivo exista antes de hacer el análisis.")

    if args.count:
        count_rows(args.csv_path)
    else:
        os.makedirs(os.path.dirname(args.html), exist_ok=True)
        summarize_data(args.csv_path, output_html=args.html)

if __name__ == "__main__":
    main()
