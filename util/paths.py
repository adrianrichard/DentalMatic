import os
import sys
from tkinter  import messagebox
def resource_path(relative_path):
    """Obtiene la ruta absoluta al recurso, funciona para desarrollo y para PyInstaller"""
    try:
        # PyInstaller crea una carpeta temporal y almacena la ruta en _MEIPASS
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")
    
    full_path = os.path.join(base_path, relative_path)
    
    # Verificar si el archivo existe
    if not os.path.exists(full_path):
        messagebox.showerror(f"ADVERTENCIA: Archivo no encontrado: {full_path}")
        # Intentar buscar en otras ubicaciones comunes
        alternative_paths = [
            os.path.join(os.path.abspath("."), relative_path),
            os.path.join(os.path.dirname(os.path.abspath(__file__)), relative_path),
            os.path.join(os.path.abspath("."), "..", relative_path)
        ]
        
        for alt_path in alternative_paths:
            if os.path.exists(alt_path):
                messagebox.showerror(f"Encontrado en ubicación alternativa: {alt_path}")
                return alt_path
    
    return full_path

def get_image_path(image_name):
    """Obtiene la ruta completa de una imagen"""
    return resource_path(os.path.join('imagenes', image_name))

def get_data_path(file_name):
    """Obtiene la ruta completa de un archivo de datos"""
    return resource_path(file_name)