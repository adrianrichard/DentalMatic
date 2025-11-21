#!/usr/bin/env python3
"""
Script para instalar las librerías: matplotlib, reportlab, Pillow
"""

import subprocess
import sys

def install_packages():
    # Lista de paquetes a instalar
    packages = [
        'matplotlib',
        'reportlab',
        'Pillow'
    ]
    
    print("Iniciando instalación de paquetes...")
    
    for package in packages:
        try:
            print(f"\nInstalando {package}...")
            # Ejecutar pip install para cada paquete
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])
            print(f"✓ {package} instalado correctamente")
            
        except subprocess.CalledProcessError as e:
            print(f"✗ Error al instalar {package}: {e}")
            return False
    
    print("\n¡Todas las librerías han sido instaladas exitosamente!")
    return True

if __name__ == "__main__":
    install_packages()