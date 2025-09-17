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
