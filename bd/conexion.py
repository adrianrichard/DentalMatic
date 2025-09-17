import sqlite3
import os
from tkinter import messagebox

class Conexion():
    # Variable de clase para rastrear todas las instancias
    _instancias = []
    
    def __init__(self, ruta_bd=None):
        # Obtener la ruta base del directorio de bd (un nivel superior al script actual)
        if ruta_bd is None:
            BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            BD_DIR = os.path.join(BASE_DIR, 'bd')
            
            # Crear la carpeta bd si no existe
            if not os.path.exists(BD_DIR):
                try:
                    os.makedirs(BD_DIR)
                    messagebox.showinfo(f"Carpeta 'bd' creada en: {BD_DIR}")
                except OSError as e:
                    messagebox.showerror("Error", f"No se pudo crear la carpeta 'bd': {e}")
                    return
            
            self.ruta_bd = os.path.join(BD_DIR, 'consultorioMyM.sqlite3')
        else:
            self.ruta_bd = ruta_bd
            
        self.db = None  # Inicializar explícitamente como None
        self.cur = None  # Inicializar explícitamente como None
        Conexion._instancias.append(self)

    def comprobar_bd(self):
        return os.path.isfile(self.ruta_bd)
    
    def conectar(self):
        try:
            self.db = sqlite3.connect(self.ruta_bd)
            return self.db
        except sqlite3.Error as e:
            messagebox.showerror("Advertencia", f"Error al conectar a la base de datos \n {e}")
            return None

    def obtener_cursor(self):
        if self.db:
            self.cur = self.db.cursor()
            return self.cur
        return None

    def buscar_usuario(self, username, password):
        try:
            if not self.cur:
                self.conectar()
                self.obtener_cursor()

            self.cur.execute('SELECT nombre_usuario, pass_usuario, tipo_usuario FROM usuarios WHERE nombre_usuario = ? AND pass_usuario = ?', (username, password))
            registro = self.cur.fetchone()
            return registro
        except sqlite3.Error as e:
            messagebox.showerror("Advertencia", f"Error al conectar a la base de datos \n {e}")
            return None

    def cerrar_bd(self):
        """Cierra la conexión de manera segura, evitando errores con None"""
        # Verificar que cur existe y no es None antes de cerrarlo
        if hasattr(self, 'cur') and self.cur is not None:
            try:
                self.cur.close()
            except:
                pass  # Ignorar errores al cerrar

        # Verificar que db existe y no es None antes de cerrarlo
        if hasattr(self, 'db') and self.db is not None:
            try:
                self.db.close()
            except:
                pass  # Ignorar errores al cerrar

        # Limpiar las referencias
        self.cur = None
        self.db = None

    @classmethod
    def cerrar_todas_conexiones(cls):
        """Cierra todas las conexiones a la base de datos de manera segura"""
        for instancia in cls._instancias:
            try:
                instancia.cerrar_bd()
            except Exception as e:
                messagebox.showerror(f"Advertencia: Error al cerrar conexión: {e}")
                # Continuar con las demás instancias

    @classmethod
    def reconectar_todas(cls):
        """Reconecta todas las instancias después de un cambio de BD"""
        for instancia in cls._instancias:
            try:
                if hasattr(instancia, 'ruta_bd'):
                    # Cerrar primero si hay conexiones existentes
                    instancia.cerrar_bd()
                    # Reconectar
                    instancia.db = sqlite3.connect(instancia.ruta_bd)
                    instancia.cur = instancia.db.cursor()
            except Exception as e:
                messagebox.showerror(f"Error al reconectar: {e}")

    def crear_bd_login(self):
        #self.ruta_bd
        sql_script = """
        -- Tabla Odontologos
        CREATE TABLE IF NOT EXISTS Odontologos (
            Matricula INTEGER NOT NULL,
            Apellido_odontologo TEXT NOT NULL,
            Nombre_odontologo VARCHAR(50),
            CONSTRAINT Odontologos_PK PRIMARY KEY (Matricula)
        );

        -- Tabla Pacientes
        CREATE TABLE IF NOT EXISTS Pacientes (
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            NOMBRE VARCHAR(50) NOT NULL,
            APELLIDO VARCHAR(50) NOT NULL,
            domicilio VARCHAR(50),
            telefono INTEGER,
            email VARCHAR(50),
            obrasocial VARCHAR(50),
            nrosocio INTEGER,
            edad INTEGER,
            fechanacimiento DATE
        );

        -- Tabla Odontogramas
        CREATE TABLE IF NOT EXISTS Odontogramas (
            id_odontograma INTEGER NOT NULL,
            dni_paciente INTEGER NOT NULL,
            fecha DATE NOT NULL,
            odontologo INTEGER NOT NULL DEFAULT '',
            CONSTRAINT ODONTOGRAMAS_PK PRIMARY KEY(id_odontograma),
            CONSTRAINT Odontogramas_Odontologos_FK FOREIGN KEY(odontologo) REFERENCES Odontologos(Matricula),
            CONSTRAINT Odontogramas_Pacientes_FK FOREIGN KEY(dni_paciente) REFERENCES Pacientes(ID)
        );

        -- Tabla Prestaciones
        CREATE TABLE IF NOT EXISTS Prestaciones (
            id_prestacion INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            tipo_prestacion TEXT NOT NULL,
            fecha DATE NOT NULL,
            paciente INTEGER NOT NULL,
            odontologo INTEGER NOT NULL
        );

        -- Tabla Turnos
        CREATE TABLE IF NOT EXISTS Turnos (
            Fecha DATE NOT NULL,
            Hora TIME NOT NULL,
            Paciente TEXT NOT NULL,
            Odontologo NUMERIC NOT NULL,
            Prestacion TEXT NOT NULL,
            CONSTRAINT Turnos_PK PRIMARY KEY(Fecha, Hora),
            CONSTRAINT Turnos_Odontologos_FK FOREIGN KEY(Odontologo) REFERENCES Odontologos(Matricula)
        );

        -- Tabla dientes
        CREATE TABLE IF NOT EXISTS dientes (
            nro INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            nro_diente INTEGER,
            id_odonto INTEGER,
            d TEXT DEFAULT NULL,
            v TEXT DEFAULT NULL,
            m TEXT DEFAULT NULL,
            i REAL DEFAULT NULL,
            o INTEGER DEFAULT NULL,
            extraccion TEXT DEFAULT NULL,
            corona TEXT DEFAULT NULL,
            CONSTRAINT dientes_odontogramas_FK FOREIGN KEY(id_odonto) REFERENCES Odontogramas(id_odontograma)
        );

        -- Tabla usuarios
        CREATE TABLE IF NOT EXISTS usuarios (
            id_usuario INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre_usuario VARCHAR(50),
            pass_usuario VARCHAR(50),
            tipo_usuario VARCHAR(50)
        );

        -- Crear índice para Prestaciones
        CREATE INDEX IF NOT EXISTS Prestaciones_id_prestacion_IDX ON Prestaciones (id_prestacion);
        """
        
        try:
            # Asegurarse de que el directorio existe
            directorio = os.path.dirname(self.ruta_bd)
            if not os.path.exists(directorio):
                os.makedirs(directorio)

            # Conectar a la base de datos (se crea automáticamente si no existe)
            conexion = sqlite3.connect(self.ruta_bd)
            cursor = conexion.cursor()
            
            # Habilitar claves foráneas
            cursor.execute("PRAGMA foreign_keys = ON")
            
            # Ejecutar el script SQL completo
            cursor.executescript(sql_script)
            
            # Insertar usuario administrador por defecto
            cursor.execute("""
                INSERT OR IGNORE INTO usuarios (nombre_usuario, pass_usuario, tipo_usuario) 
                VALUES ('admin', 'admin', 'administrador')
            """)
            
            # Confirmar los cambios
            conexion.commit()            

        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Error al crear la base de datos: {e}")
        finally:
            # Cerrar la conexión
            if conexion:
                conexion.close()