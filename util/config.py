from PIL import ImageTk, Image
from tkinter import messagebox
import re
import os

# Obtener la ruta base del directorio de imágenes (un nivel superior al script actual)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMAGENES_DIR = os.path.join(BASE_DIR, 'imagenes')

def obtener_ruta_imagen(nombre_archivo):
    """Obtiene la ruta completa de una imagen en la carpeta 'imagenes'"""
    return os.path.join(IMAGENES_DIR, nombre_archivo)

def leer_imagen(nombre_archivo, tamaño, mantener_proporciones=True):
    """Carga y redimensiona una imagen desde la carpeta 'imagenes'"""
    try:
        # Obtener la ruta completa de la imagen
        full_path = obtener_ruta_imagen(nombre_archivo)
        
        # Verificar si el archivo existe
        if not os.path.exists(full_path):
            messagebox.showerror("Error", f"Imagen no encontrada: {nombre_archivo}")
            return None
        
        img = Image.open(full_path)
        
        if mantener_proporciones:
            # Calcular nuevo tamaño manteniendo proporciones
            ancho_original, alto_original = img.size
            ancho_deseado, alto_deseado = tamaño
            
            # Calcular ratios
            ratio_ancho = ancho_deseado / ancho_original
            ratio_alto = alto_deseado / alto_original
            
            # Usar el ratio más pequeño para mantener proporciones
            ratio = min(ratio_ancho, ratio_alto)
            
            nuevo_ancho = int(ancho_original * ratio)
            nuevo_alto = int(alto_original * ratio)
            
            # Redimensionar manteniendo proporciones
            img = img.resize((nuevo_ancho, nuevo_alto), Image.Resampling.LANCZOS)
        else:
            # Redimensionar forzando el tamaño exacto
            img = img.resize(tamaño, Image.Resampling.LANCZOS)
        
        return ImageTk.PhotoImage(img)
        
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo cargar la imagen: {str(e)}")
        return None

def centrar_ventana(ventana, aplicacion_ancho, aplicacion_largo):
    """Centra una ventana en la pantalla"""
    pantalla_ancho = ventana.winfo_screenwidth()
    pantalla_largo = ventana.winfo_screenheight()
    x = int((pantalla_ancho/2) - (aplicacion_ancho/2))
    y = int((pantalla_largo/2) - (aplicacion_largo/2))
    return ventana.geometry(f"{aplicacion_ancho}x{aplicacion_largo}+{x}+{y}")

def definir_fuente():
    """Define la fuente normal"""
    return ('Arial', 12)

def definir_fuente_bold():
    """Define la fuente en negrita"""
    return ('Arial', 12, 'bold')

def definir_color_fuente():
    """Define colores de fuente (modo claro, modo oscuro)"""
    return 'black', 'white'

def definir_color_fondo():
    """Define colores de fondo (modo claro, modo oscuro)"""
    return '#1F704B', 'gray90'

def validar_password(password):
    """Valida que la contraseña cumpla con los requisitos de seguridad"""
    if len(password) < 8:
        return False
    
    # Verificar criterios de seguridad
    tiene_minuscula = any(c.islower() for c in password)
    tiene_mayuscula = any(c.isupper() for c in password)
    tiene_numero = any(c.isdigit() for c in password)
    sin_espacios = ' ' not in password
    
    return tiene_minuscula and tiene_mayuscula and tiene_numero and sin_espacios

def validar_correo(value):
    """Valida que el formato de email sea correcto"""
    pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    return re.fullmatch(pattern, value) is not None