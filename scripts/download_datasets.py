#!/usr/bin/env python3
"""
Script para descargar datasets desde Kaggle
Sistema de Clasificación y Extracción de Información de Documentos Vehiculares
"""

import os
import subprocess
import sys
from pathlib import Path
import time

def run_command(command, description):
    """Ejecuta un comando y maneja errores"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, 
                              capture_output=True, text=True)
        print(f"✅ {description} completado")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error en {description}:")
        print(f"   Comando: {command}")
        print(f"   Error: {e.stderr}")
        return False

def download_kaggle_dataset(dataset_name, output_dir, description):
    """Descarga un dataset desde Kaggle"""
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    # Comando para descargar y descomprimir
    command = f"kaggle datasets download -d {dataset_name} -p {output_dir} --unzip"
    
    success = run_command(command, f"Descargando {description}")
    
    if success:
        # Verificar archivos descargados
        files = list(output_path.rglob("*"))
        file_count = len([f for f in files if f.is_file()])
        total_size = sum(f.stat().st_size for f in files if f.is_file()) / (1024*1024)  # MB
        
        print(f"   📊 {file_count} archivos descargados")
        print(f"   💾 Tamaño total: {total_size:.1f} MB")
        return True
    
    return False

def main():
    """Función principal para descargar todos los datasets"""
    print("🚀 DESCARGA DE DATASETS - VEHICLE DOCUMENT SYSTEM")
    print("=" * 60)
    
    # Verificar que kaggle esté configurado
    if not os.path.exists(os.path.expanduser("~/.kaggle/kaggle.json")):
        print("❌ Kaggle API no configurada.")
        print("   Configure Kaggle API primero:")
        print("   1. Coloque kaggle.json en ~/.kaggle/")
        print("   2. Ejecute: chmod 600 ~/.kaggle/kaggle.json")
        sys.exit(1)
    
    # Verificar conexión a Kaggle
    print("🔍 Verificando conexión a Kaggle...")
    if not run_command("kaggle datasets list --max-size 1", "Test de conexión Kaggle"):
        print("❌ No se pudo conectar a Kaggle. Verifique sus credenciales.")
        sys.exit(1)
    
    # Crear directorio base
    data_dir = Path("data/raw")
    data_dir.mkdir(parents=True, exist_ok=True)
    
    # Datasets a descargar (ordenados por prioridad y tamaño)
    datasets = [
        {
            "name": "andrewmvd/car-plate-detection",
            "folder": "car_plate_detection",
            "description": "Car License Plate Detection (433 images)",
            "priority": 1
        },
        {
            "name": "dataclusterlabs/bike-and-car-odometer-dataset",
            "folder": "odometer_dataset", 
            "description": "Vehicle Odometer Dataset",
            "priority": 2
        },
        {
            "name": "trainingdatapro/text-detection-in-the-documents",
            "folder": "document_ocr",
            "description": "Document OCR Dataset",
            "priority": 3
        },
        {
            "name": "venkatsairo4899/ev-population-data",
            "folder": "ev_registration",
            "description": "Electric Vehicle Registration Data",
            "priority": 4
        }
    ]
    
    print(f"\n📦 Descargando {len(datasets)} datasets...")
    print("-" * 50)
    
    successful_downloads = 0
    start_time = time.time()
    
    for i, dataset in enumerate(datasets, 1):
        print(f"\n[{i}/{len(datasets)}] {dataset['description']}")
        
        output_path = data_dir / dataset['folder']
        
        # Verificar si ya existe
        if output_path.exists() and list(output_path.iterdir()):
            print(f"⏩ Dataset ya existe en {output_path}")
            successful_downloads += 1
            continue
        
        # Descargar dataset
        success = download_kaggle_dataset(
            dataset['name'],
            output_path,
            dataset['description']
        )
        
        if success:
            successful_downloads += 1
        else:
            print(f"⚠️  Falló la descarga de {dataset['description']}")
            
        # Pausa pequeña entre descargas
        if i < len(datasets):
            time.sleep(2)
    
    # Resumen final
    elapsed_time = time.time() - start_time
    print("\n" + "=" * 60)
    print("📊 RESUMEN DE DESCARGA:")
    print(f"   ✅ Exitosos: {successful_downloads}/{len(datasets)}")
    print(f"   ⏱️  Tiempo total: {elapsed_time/60:.1f} minutos")
    
    if successful_downloads == len(datasets):
        print("\n🎉 ¡Todos los datasets descargados exitosamente!")
    elif successful_downloads >= 3:
        print(f"\n✅ {successful_downloads} datasets descargados. Suficiente para comenzar.")
    else:
        print(f"\n⚠️  Solo {successful_downloads} datasets descargados. Puede continuar con los disponibles.")
    
    # Mostrar estructura final
    print("\n📁 Estructura de datos:")
    for dataset in datasets:
        folder_path = data_dir / dataset['folder']
        if folder_path.exists():
            file_count = len(list(folder_path.rglob("*")))
            print(f"   {dataset['folder']}/  ({file_count} archivos)")
    
    print(f"\n🚀 Listo para comenzar con la exploración de datos!")
    print("   Siguiente paso: jupyter notebook notebooks/01_data_exploration.ipynb")

if __name__ == "__main__":
    main()
