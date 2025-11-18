import random
import sqlite3
from datetime import datetime, timedelta
import os

# ---------------------------
# Configuración de rutas
# ---------------------------

# Obtener el directorio actual del script
script_dir = os.path.dirname(os.path.abspath(__file__))
# Subir un nivel y apuntar a la carpeta bd
bd_dir = os.path.join(os.path.dirname(script_dir), 'bd')
# Ruta completa de la base de datos
db_path = os.path.join(bd_dir, 'consultorioMyM.sqlite3')

# ---------------------------
# Configuración de datos base
# ---------------------------

nombres = ["Juan", "Maria", "Pedro", "Ana", "Luis", "Sofia", "Diego", "Lucia", "Carlos", "Valeria",
           "Esteban", "Laura", "Marcos", "Paula", "Ricardo", "Natalia", "Hernan", "Clara", "Jorge", "Cecilia"]
apellidos = ["Gomez", "Lopez", "Martinez", "Fernandez", "Perez", "Acosta", "Ramirez", "Sosa", "Mendoza", "Diaz",
             "Torres", "Dominguez", "Alvarez", "Suarez", "Benitez", "Rojas", "Flores", "Medina", "Castro", "Vega"]

calles = [
    "San Martín", "Urquiza", "Echagüe", "Corrientes", "Monte Caseros", "La Rioja",
    "Belgrano", "Andrés Pazos", "Italia", "Buenos Aires", "Gualeguaychú",
    "25 de Mayo", "Perú", "México", "España", "Chile", "Brasil", "Andrade", "Estrada", "Paraguay"
]

obras_sociales = ["OSDOP", "OSPLA", "IOSPER", "PAMI", "UOCRA", "OSPRERA"]

codigos_area = ["343", "344", "345", "347"]

# Rango de fechas de nacimiento
fecha_inicio = datetime(1980, 1, 1)
fecha_fin = datetime(2010, 12, 31)
rango_dias = (fecha_fin - fecha_inicio).days

# ---------------------------
# Conexión a la base de datos
# ---------------------------

def conectar_bd():
    """Conectar a la base de datos SQLite en la carpeta bd"""
    try:
        # Crear la carpeta bd si no existe
        os.makedirs(bd_dir, exist_ok=True)
        print(f"Ruta de la base de datos: {db_path}")
        
        conn = sqlite3.connect(db_path)
        return conn
    except sqlite3.Error as e:
        print(f"Error conectando a la base de datos: {e}")
        return None

def crear_tabla(conn):
    """Crear la tabla Pacientes si no existe"""
    try:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Pacientes (
                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                NOMBRE VARCHAR(50) NOT NULL,
                APELLIDO VARCHAR(50) NOT NULL,
                domicilio VARCHAR(100),
                telefono VARCHAR(20),
                email VARCHAR(100),
                obrasocial VARCHAR(50),
                nrosocio INTEGER,
                edad INTEGER,
                fechanacimiento DATE
            )
        ''')
        conn.commit()
        print("Tabla 'Pacientes' creada/verificada correctamente")
    except sqlite3.Error as e:
        print(f"Error creando la tabla: {e}")

def insertar_pacientes(conn, cantidad=100):
    """Insertar pacientes en la base de datos"""
    cursor = conn.cursor()
    emails_generados = set()
    pacientes_insertados = 0
    
    print(f"Generando {cantidad} pacientes...")
    
    for i in range(cantidad):
        nombre = random.choice(nombres)
        apellido = random.choice(apellidos)
        
        # Generar email único
        base_email = f"{nombre.lower()}.{apellido.lower()}"
        email = f"{base_email}@mail.com"
        contador = 1
        while email in emails_generados:
            email = f"{base_email}{contador}@mail.com"
            contador += 1
        emails_generados.add(email)

        domicilio = f"{random.choice(calles)} {random.randint(10, 999)}, Paraná, Entre Ríos"
        telefono = f"{random.choice(codigos_area)}{random.randint(1000000, 9999999)}"
        obra = random.choice(obras_sociales)
        nrosocio = random.randint(1, 1500)

        # Fecha de nacimiento aleatoria
        fecha_nac = fecha_inicio + timedelta(days=random.randint(0, rango_dias))
        fecha_str = fecha_nac.strftime("%Y-%m-%d")

        # Edad calculada
        hoy = datetime.now()
        edad = hoy.year - fecha_nac.year - ((hoy.month, hoy.day) < (fecha_nac.month, fecha_nac.day))

        try:
            # Insertar en la base de datos
            cursor.execute('''
                INSERT INTO Pacientes 
                (NOMBRE, APELLIDO, domicilio, telefono, email, obrasocial, nrosocio, edad, fechanacimiento)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (nombre, apellido, domicilio, telefono, email, obra, nrosocio, edad, fecha_str))
            
            pacientes_insertados += 1
            
            # Mostrar progreso cada 10 registros
            if (i + 1) % 10 == 0:
                print(f"Progreso: {i + 1}/{cantidad} pacientes generados")
                
        except sqlite3.IntegrityError as e:
            print(f"Error de integridad (posible email duplicado): {email} - {e}")
        except sqlite3.Error as e:
            print(f"Error insertando paciente: {e}")
    
    conn.commit()
    return pacientes_insertados

def contar_pacientes(conn):
    """Contar el total de pacientes en la base de datos"""
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM Pacientes")
    return cursor.fetchone()[0]

def mostrar_estadisticas(conn):
    """Mostrar estadísticas de los datos insertados"""
    cursor = conn.cursor()
    
    print("\n" + "="*50)
    print("ESTADÍSTICAS DE LA BASE DE DATOS")
    print("="*50)
    
    # Total de pacientes
    total = contar_pacientes(conn)
    print(f"👥 Total de pacientes: {total}")
    
    # Distribución por obra social
    cursor.execute('''
        SELECT obrasocial, COUNT(*) as cantidad 
        FROM Pacientes 
        GROUP BY obrasocial 
        ORDER BY cantidad DESC
    ''')
    print("\n Distribución por obra social:")
    for obra, cantidad in cursor.fetchall():
        print(f"   {obra}: {cantidad} pacientes")
    
    # Rango de edades
    cursor.execute('SELECT MIN(edad), MAX(edad), AVG(edad) FROM Pacientes')
    min_edad, max_edad, avg_edad = cursor.fetchone()
    print(f"\nEdades: Mínima={min_edad}, Máxima={max_edad}, Promedio={avg_edad:.1f}")
    
    # Últimos 5 pacientes insertados
    cursor.execute('''
        SELECT ID, NOMBRE, APELLIDO, telefono, obrasocial 
        FROM Pacientes 
        ORDER BY ID DESC 
        LIMIT 5
    ''')
    print(f"\nÚltimos 5 pacientes insertados:")
    for paciente in cursor.fetchall():
        print(f" ID: {paciente[0]}, {paciente[1]} {paciente[2]}, Tel: {paciente[3]}, Obra: {paciente[4]}")

def verificar_estructura_carpetas():
    """Verificar y mostrar la estructura de carpetas"""
    print("Verificando estructura de carpetas...")
    print(f"Directorio del script: {script_dir}")
    print(f"Carpeta de BD: {bd_dir}")
    print(f"Archivo de BD: {db_path}")
    
    # Verificar si la carpeta bd existe
    if os.path.exists(bd_dir):
        print("Carpeta 'bd' encontrada")
    else:
        print("Carpeta 'bd' no existe, se creará automáticamente")

# ---------------------------
# Ejecución principal
# ---------------------------

def main():
    print("INICIANDO GENERADOR DE BASE DE DATOS DE PACIENTES")
    print("="*60)
    
    # Verificar estructura de carpetas
    verificar_estructura_carpetas()
    print("-" * 60)
    
    # Conectar a la base de datos
    conn = conectar_bd()
    if conn is None:
        return
    
    try:
        # Crear tabla
        crear_tabla(conn)
        
        # Contar pacientes existentes
        pacientes_existentes = contar_pacientes(conn)
        print(f"Pacientes existentes en la base de datos: {pacientes_existentes}")
        
        # Preguntar cuántos pacientes agregar
        try:
            cantidad = int(input("\n¿Cuántos pacientes deseas generar? (default: 100): ") or "100")
        except ValueError:
            cantidad = 100
        
        # Insertar pacientes
        if cantidad > 0:
            insertados = insertar_pacientes(conn, cantidad)
            print(f"\n {insertados} pacientes insertados correctamente")
        
        # Mostrar estadísticas
        mostrar_estadisticas(conn)
        
        print(f"\n Base de datos guardada en: {db_path}")
        
    finally:
        # Cerrar conexión
        conn.close()
        print("\n Conexión a la base de datos cerrada")

if __name__ == "__main__":
    main()
    
""""
import random
from datetime import datetime, timedelta

# ---------------------------
# Configuración de datos base
# ---------------------------

nombres = ["Juan", "Maria", "Pedro", "Ana", "Luis", "Sofia", "Diego", "Lucia", "Carlos", "Valeria",
           "Esteban", "Laura", "Marcos", "Paula", "Ricardo", "Natalia", "Hernan", "Clara", "Jorge", "Cecilia"]
apellidos = ["Gomez", "Lopez", "Martinez", "Fernandez", "Perez", "Acosta", "Ramirez", "Sosa", "Mendoza", "Diaz",
             "Torres", "Dominguez", "Alvarez", "Suarez", "Benitez", "Rojas", "Flores", "Medina", "Castro", "Vega"]

calles = [
    "San Martín", "Urquiza", "Echagüe", "Corrientes", "Monte Caseros", "La Rioja",
    "Belgrano", "Andrés Pazos", "Italia", "Buenos Aires", "Gualeguaychú",
    "25 de Mayo", "Perú", "México", "España", "Chile", "Brasil", "Andrade", "Estrada", "Paraguay"
]

obras_sociales = ["OSDOP", "OSPLA", "IOSPER", "PAMI", "UOCRA", "OSPRERA"]

# Rango de fechas de nacimiento
fecha_inicio = datetime(1980, 1, 1)
fecha_fin = datetime(2010, 12, 31)
rango_dias = (fecha_fin - fecha_inicio).days

# ---------------------------
# Generación de registros
# ---------------------------

print("INSERT INTO Pacientes (ID, NOMBRE, APELLIDO, domicilio, telefono, email, obrasocial, nrosocio, edad, fechanacimiento) VALUES")

for i in range(100):
    # ID = DNI ficticio entre 20 y 45 millones
    dni = random.randint(20000000, 45000000)

    nombre = random.choice(nombres)
    apellido = random.choice(apellidos)

    domicilio = f"{random.choice(calles)} {random.randint(10, 999)}, Paraná"

    telefono = "3434" + str(random.randint(100000, 999999))  # 10 dígitos

    email = f"{nombre.lower()}.{apellido.lower()}@mail.com"

    obra = random.choice(obras_sociales)

    nrosocio = random.randint(1, 1500)

    # Fecha de nacimiento aleatoria
    fecha_nac = fecha_inicio + timedelta(days=random.randint(0, rango_dias))
    fecha_str = fecha_nac.strftime("%Y-%m-%d")

    # Edad calculada
    hoy = datetime.now()
    edad = hoy.year - fecha_nac.year - ((hoy.month, hoy.day) < (fecha_nac.month, fecha_nac.day))

    # Imprimir fila SQL
    end_char = "," if i < 99 else ";"  # última fila termina con ;
    print(f"({dni}, '{nombre}', '{apellido}', '{domicilio}', '{telefono}', '{email}', '{obra}', {nrosocio}, {edad}, '{fecha_str}'){end_char}")
"""