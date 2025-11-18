import random
import sqlite3
from datetime import datetime, timedelta
import os

# Obtener el directorio actual del script
script_dir = os.path.dirname(os.path.abspath(__file__))
# Subir un nivel y apuntar a la carpeta bd
bd_dir = os.path.join(os.path.dirname(script_dir), 'bd')
# Ruta completa de la base de datos
db_path = os.path.join(bd_dir, 'consultorioMyM.sqlite3')

nombres = ["JUAN", "MARIA", "PEDRO", "ANA", "LUIS", "SOFIA", "DIEGO", "LUCIA", "CARLOS", "VALERIA",
           "ESTEBAN", "LAURA", "MARCOS", "PAULA", "RICARDO", "NATALIA", "HERNAN", "CLARA", "JORGE", "CECILIA"]
apellidos = [
    "GOMEZ", "RODRIGUEZ", "GONZALEZ", "FERNANDEZ", "LOPEZ", "DIAZ", "MARTINEZ", "PEREZ", "GARCIA", "SANCHEZ",
    "ROMERO", "SOSA", "ALVAREZ", "TORRES", "RUIZ", "RAMIREZ", "FLORES", "ACOSTA", "BENITEZ", "MEDINA",
    "HERRERA", "SUAREZ", "AGUIRRE", "GIMENEZ", "GUTIERREZ", "MOLINA", "SILVA", "CASTRO", "ROJAS", "ORTIZ",
    "NÚÑEZ", "LUNA", "JUAREZ", "CABRERA", "RIOS", "MORALES", "GODOY", "MORENO", "FERREYRA", "DOMINGUEZ",
    "CARRIZO", "PERALTA", "CASTILLO", "LEDESMA", "QUIROGA", "MENDOZA", "VEGA", "VERA", "MUÑOZ", "OJEDA",
    "PONCE", "VAZQUEZ", "CARDOZO", "CORREA", "VILLALBA", "FIGUEROA", "LUCERO", "PAZ", "RIVAROLA", "CORDOBA",
    "BARRIOS", "MAIDANA", "MANSILLA", "FARIAS", "ROLDAN", "MARQUEZ", "VILLAGRA", "CORONEL", "ARIAS", "ESCOBAR",
    "AGUILAR", "SORIA", "MOYANO", "OLIVERA", "CAMPOS", "DUARTE", "PAEZ", "RAMOS", "SOTO", "VALDEZ",
    "LEGUIZAMON", "CACERES", "YAÑEZ", "TOLEDO", "FRANCO", "PINTO", "CARABALLO", "VILLAFAÑE", "NAVARRO", "LOPEZ",
    "ARCE", "MALDONADO", "PEREYRA", "HEREDIA", "FARIAS", "CHAVEZ", "VELAZQUEZ", "MONTOYA", "RICO", "CRUZ",
    "SALINAS", "ZARATE", "MIRANDA", "SEGURA", "VARGAS", "CACERES", "BUSTOS", "LORENZO", "COSTA", "IBAÑEZ",
    "LESCANO", "ALONSO", "VILLALBA", "RIVERO", "BERNAL", "ROCHA", "PADILLA", "VILLANUEVA", "VERGARA", "VILLA",
    "CABRAL", "ARAYA", "ARAVENA", "BAEZ", "BLANCO", "BRITO", "CALVO", "CARDENAS", "CARRASCO", "CASAS",
    "CASTILLO", "COLLADO", "CONDE", "CONTRERAS", "CORTES", "CUEVAS", "DELGADO", "DURAN", "ESPINOZA", "ESTEBAN",
    "FERRER", "FONSECA", "FUENTES", "GALLARDO", "GARRIDO", "GUERRERO", "GUZMAN", "IGLESIAS", "LEON", "LIRA",
    "LLORENTE", "LOBATO", "LORCA", "LOSA", "MADRID", "MARIN", "MENDEZ", "MESA", "MIGUEZ", "MILLAN",
    "MONTERO", "MORA", "MORO", "MURILLO", "NARANJO", "NIETO", "ORTEGA", "PALACIOS", "PARRA", "PASTOR",
    "PEÑA", "PRIETO", "QUESADA", "QUINTERO", "REDONDO", "REINA", "REQUENA", "REVUELTA", "REY", "REYES",
    "RIVAS", "ROBLES", "ROJO", "ROS", "ROSALES", "ROSARIO", "RUBIO", "SALAS", "SALAZAR", "SALGADO",
    "SALVADOR", "SANCHO", "SANTANA", "SANTOS", "SARMIENTO", "SEPÚLVEDA", "SERRANO", "SOLANO", "SOLIS", "SORDO",
    "SORIANO", "TELLEZ", "TIRADO", "TORO", "TREJO", "TRUJILLO", "UREÑA", "VALERO", "VALLE", "VARELA",
    "VENTURA", "VICENTE", "VIDAL", "VILA", "ZAMBRANO", "ZAPATA", "ZÚÑIGA", "ALARCON", "ALBA", "ALBERDI",
    "ALCANTARA", "ALEM", "ALTAMIRANO", "AMAYA", "ANDRADE", "ARAUJO", "AREVALO", "ARROYO", "AVILA", "AYALA",
    "AZCONA", "BALLESTEROS", "BARRETO", "BARRIENTOS", "BARROS", "BECERRA", "BELTRAN", "BERMÚDEZ", "BETANCUR", "BOLAÑOS",
    "BONILLA", "BORGES", "BORJA", "BOTERO", "BRAVO", "BURGOS", "BUSTAMANTE", "CABAL", "CABALLERO", "CABEZA",
    "CADENA", "CALDERON", "CAMACHO", "CAMPO", "CANO", "CANTILLO", "CARDENAS", "CARMONA", "CARO", "CARRILLO",
    "CARTAGENA", "CASADO", "CASARES", "CASAS", "CASTAÑEDA", "CASTELLANOS", "CEBALLOS", "CEPEDA", "CERDA", "CERVANTES",
    "CHACON", "CHAVERRA", "CIFUENTES", "CISNEROS", "COBO", "COLMENARES", "CONDE", "CORDERO", "CORRAL", "CORTAZAR",
    "CRESPO", "CUELLAR", "CUENCA", "CUERVO", "CUESTA", "DAVILA", "DE LA CRUZ", "DE LA TORRE", "DEL VALLE", "DELGADO",
    "DIEZ", "DUEÑAS", "ECHEVERRIA", "ELORZA", "ENRIQUEZ", "ESCALANTE", "ESCUDERO", "ESPINOSA", "ESQUIVEL", "ESTRADA",
    "FAJARDO", "FALCON", "FERRERO", "FIGUERAS", "FONTALVO", "FRIAS", "GALAN", "GALINDO", "GALLARDO", "GALLEGOS",
    "GALVAN", "GAMEZ", "GARAY", "GARNICA", "GARZA", "GIL", "GIRALDO", "GRAJALES", "GRANADOS", "GUERRA",
    "GUILLEN", "GURIDI", "HERNANDO", "HIDALGO", "HINCAPIE", "HOYOS", "HUERTA", "IBAÑEZ", "ISAZA", "IZQUIERDO",
    "JAIMES", "JARAMILLO", "JEREZ", "JIMENEZ", "LADINO", "LARA", "LARROSA", "LEIVA", "LEMUS", "LEON",
    "LINARES", "LIZARAZO", "LLANOS", "LONDOÑO", "LONGAS", "LOPERA", "LORA", "LORENZO", "LOSADA", "LOZANO",
    "MACIAS", "MADERO", "MAESTRE", "MALAGON", "MANCILLA", "MANRIQUE", "MANZANO", "MARQUES", "MARTIN", "MARTINIC",
    "MASCARENO", "MATEO", "MAYORAL", "MENA", "MERINO", "MESA", "MESTRE", "MILLAN", "MIRELES", "MOJICA",
    "MOLES", "MOLINA", "MOLL", "MONTALVO", "MONTAÑEZ", "MONTEJO", "MONTENEGRO", "MONTES", "MORA", "MORALES",
    "MORENO", "MORGADO", "MORO", "MOYA", "MUNGUIA", "MURCIA", "NAVA", "NAVAS", "NIETO", "NOGUEIRA",
    "NOVA", "NOVOA", "NÚÑEZ", "OCAMPO", "OCHOA", "OLIVA", "OLIVEIRA", "OLIVER", "OLIVEROS", "ORDOÑEZ",
    "ORELLANA", "ORTEGA", "ORTIZ", "OSPINA", "OSSA", "OTERO", "PACHECO", "PADRON", "PALACIO", "PALOMINO",
    "PAREJA", "PARRA", "PASCUAL", "PASTRANA", "PATINO", "PAVON", "PEDRAZA", "PELAEZ", "PEÑARANDA", "PEÑATE",
    "PEREA", "PERDOMO", "PEREZ", "PIEDRAHITA", "PIZARRO", "PLAZA", "POLANCO", "POLO", "PONCE", "PORRAS",
    "PORTILLO", "POSADA", "POVEDA", "PRADO", "PRIETO", "PUENTE", "PULIDO", "QUESADA", "QUEZADA", "QUIROZ"
]
calles = [
    "SAN MARTIN", "URQUIZA", "ECHAGÜE", "CORRIENTES", "MONTE CASEROS", "LA RIOJA", "BELGRANO", "ANDRES PAZOS", "ITALIA",
    "BUENOS AIRES", "GUALEGUAYCHÚ", "25 DE MAYO", "PERÚ", "MEXICO", "ESPAÑA", "CHILE", "BRASIL", "ANDRADE", "ESTRADA", "PARAGUAY"
]
obras_sociales = ["OSDOP", "OSPLA", "IOSPER", "PAMI", "UOCRA", "OSPRERA"]
codigos_area = ["343", "342", "341"]
apellidos_odontologos = ["GUTIERREZ", "LOPEZ", "MARTINEZ", "RODRIGUEZ", "FERNANDEZ", "PEREZ", "GOMEZ", "DIAZ", "SILVA", "ROMERO"]

matriculas_odontologos = [12345, 23456, 34567, 45678, 56789, 67890, 78901, 89012, 90123, 11223]

# Rango de fechas de nacimiento
fecha_inicio = datetime(1980, 1, 1)
fecha_fin = datetime(2010, 12, 31)
rango_dias = (fecha_fin - fecha_inicio).days

def conectar_bd():
    try:
        conn = sqlite3.connect(db_path)
        return conn
    except sqlite3.Error as e:
        print(f"Error conectando a la base de datos: {e}")
        return None

def insertar_pacientes(conn, cantidad=100):
    cursor = conn.cursor()
    emails_generados = set()

    for i in range(cantidad):
        nombre = random.choice(nombres)
        apellido = random.choice(apellidos)
        dni = random.randint(20000000, 45000000)
        base_email = f"{nombre.lower()}.{apellido.lower()}"
        email = f"{base_email}@mail.com"
        contador = 1
        while email in emails_generados:
            email = f"{base_email}{contador}@mail.com"
            contador += 1
        emails_generados.add(email)

        domicilio = f"{random.choice(calles)} {random.randint(10, 999)}"
        telefono = f"{random.choice(codigos_area)}{random.randint(1000000, 9999999)}"
        obra = random.choice(obras_sociales)
        nrosocio = random.randint(1, 1500)

        fecha_nac = fecha_inicio + timedelta(days=random.randint(0, rango_dias))
        fecha_str = fecha_nac.strftime("%Y-%m-%d")

        hoy = datetime.now()
        edad = hoy.year - fecha_nac.year - ((hoy.month, hoy.day) < (fecha_nac.month, fecha_nac.day))

        try:
            cursor.execute('''
                INSERT INTO Pacientes 
                (ID, NOMBRE, APELLIDO, domicilio, telefono, email, obrasocial, nrosocio, edad, fechanacimiento)
                VALUES (?,?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (dni, nombre, apellido, domicilio, telefono, email, obra, nrosocio, edad, fecha_str))

        except sqlite3.Error as e:
            print(f"Error insertando paciente: {e}")

    conn.commit()

def insertar_odontologos(conn):
    cursor = conn.cursor()

    for i in range(10):
        matricula = matriculas_odontologos[i]
        apellido = apellidos_odontologos[i]
        nombre = random.choice(nombres)

        try:
            cursor.execute('''
                INSERT INTO Odontologos 
                (Matricula, Apellido_odontologo, Nombre_odontologo)
                VALUES (?, ?, ?)
            ''', (matricula, apellido, nombre))

        except sqlite3.Error as e:
            print(f"Error insertando odontólogo: {e}")

    conn.commit()

def generar_turnos(conn, cantidad=1000):
    
    PRESTACIONES = ["CONSULTA", "EXTRACCIÓN", "TRATAMIENTO DE CONDUCTO", "LIMPIEZA"]
    HORAS_TURNO = ["08:00", "08:30", "09:00", "09:30", "10:00", "10:30", "11:00", "11:30", "14:00", "14:30",
                   "15:00", "15:30", "16:00", "16:30", "17:00", "17:30", "18:00", "18:30", "19:00", "19:30", "20:00"]
    
    cursor = conn.cursor()
    
    try:
        cursor.execute("SELECT NOMBRE || ' ' || APELLIDO FROM Pacientes")
        pacientes = [row[0] for row in cursor.fetchall()]
        
        if not pacientes:
            print("No hay pacientes registrados en la base de datos")
            return 0
        
        cursor.execute("SELECT Matricula FROM Odontologos")
        odontologos = [row[0] for row in cursor.fetchall()]
        
        if not odontologos:
            print("No hay odontólogos registrados en la base de datos")
            return 0
      
        fecha_inicio = datetime(2022, 1, 1)
        fecha_fin = datetime.now()
        rango_dias = (fecha_fin - fecha_inicio).days
        
        turnos_generados = 0
        intentos = 0
        max_intentos = cantidad * 3  # Límite para evitar bucle infinito

        while turnos_generados < cantidad and intentos < max_intentos:
            # Fecha aleatoria dentro del rango
            fecha = fecha_inicio + timedelta(days=random.randint(0, rango_dias))
            
            # Solo días laborables (lunes a viernes)
            if fecha.weekday() >= 5:  # 5 = sábado, 6 = domingo
                continue
            
            fecha_str = fecha.strftime("%Y-%m-%d")
            
            # Hora aleatoria
            hora = random.choice(HORAS_TURNO)
            
            # Paciente y odontólogo aleatorios
            paciente_nombre = random.choice(pacientes)
            odontologo_matricula = random.choice(odontologos)
            
            # Prestación aleatoria
            prestacion = random.choice(PRESTACIONES)
            
            try:
                cursor.execute('''
                    INSERT INTO Turnos (Fecha, Hora, Paciente, Odontologo, Prestacion)
                    VALUES (?, ?, ?, ?, ?)
                ''', (fecha_str, hora, paciente_nombre, odontologo_matricula, prestacion))
                
                turnos_generados += 1
                intentos = 0  # Resetear intentos después de un éxito
                
                if turnos_generados % 100 == 0:
                    print(f"Progreso: {turnos_generados}/{cantidad} turnos generados")
                    
            except sqlite3.IntegrityError:
                # Turno duplicado (misma fecha y hora), continuar con siguiente intento
                intentos += 1
                continue
            except sqlite3.Error as e:
                print(f"Error insertando turno: {e}")
                intentos += 1
                continue
        
        conn.commit()
        
    except sqlite3.Error as e:
        print(f"Error en la generación de turnos: {e}")
        return 0

def main():
    conn = conectar_bd()
    if conn is None:
        return
    insertar_odontologos(conn)
    try:
        cantidad = int(input("\n¿Cuántos pacientes deseas generar? (default: 100): ") or "100")
    except ValueError:
        cantidad = 100

    if cantidad > 0:
        insertar_pacientes(conn, cantidad)
    cantidad = 1000
    generar_turnos(conn, cantidad)
    conn.close()

if __name__ == "__main__":
    main()