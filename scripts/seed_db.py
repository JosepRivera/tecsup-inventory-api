import sqlite3
import random
from datetime import datetime, timedelta

DB_PATH = "database.db"

DISPOSITIVOS = [
    {"nombre": "Laptop HP ProBook 450 G8", "marca": "HP", "tipo": "Laptop", "modelo": "ProBook 450 G8"},
    {"nombre": "Monitor Dell UltraSharp U2419H", "marca": "Dell", "tipo": "Monitor", "modelo": "U2419H"},
    {"nombre": "Laptop Lenovo ThinkPad L14", "marca": "Lenovo", "tipo": "Laptop", "modelo": "ThinkPad L14"},
    {"nombre": "Laptop Dell Latitude 5420", "marca": "Dell", "tipo": "Laptop", "modelo": "Latitude 5420"},
    {"nombre": "Monitor Samsung Odyssey G5", "marca": "Samsung", "tipo": "Monitor", "modelo": "G5"},
    {"nombre": "Impresora Epson EcoTank L3250", "marca": "Epson", "tipo": "Impresora", "modelo": "L3250"},
    {"nombre": "Proyector Epson PowerLite E20", "marca": "Epson", "tipo": "Proyector", "modelo": "PowerLite E20"},
    {"nombre": "Switch Cisco Catalyst 2960", "marca": "Cisco", "tipo": "Switch", "modelo": "2960-Plus"},
    {"nombre": "PC de Escritorio OptiPlex 7080", "marca": "Dell", "tipo": "Esritorio", "modelo": "7080 SFF"},
    {"nombre": "Monitor HP EliteDisplay E243", "marca": "HP", "tipo": "Monitor", "modelo": "E243"},
]

ESTADOS = ["Bueno", "Regular", "Malo", "En mantenimiento"]
UBICACIONES = [
    ("Pabellón J", "Lab 302", "Armario A1"),
    ("Pabellón J", "Lab 305", "Armario B2"),
    ("Pabellón F", "Lab 101", "Armario C1"),
    ("Pabellón G", "Lab 202", "Armario D3"),
]

def seed():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    
    print(f"Conectado a {DB_PATH}")
    
    # Crear algunas sesiones
    TECNICOS = ["Kevin", "Maria Lopez", "Juan Perez", "Ana Garcia", "Diego Rios"]
    
    for pab, lab, arm in UBICACIONES:
        creada_en = datetime.now() - timedelta(days=random.randint(1, 30))
        tecnico = random.choice(TECNICOS)
        cursor = conn.execute(
            "INSERT INTO sesiones (tecnico, pabellon, laboratorio, armario, activa, creada_en) VALUES (?, ?, ?, ?, ?, ?)",
            (tecnico, pab, lab, arm, 0, creada_en.strftime("%Y-%m-%d %H:%M:%S"))
        )
        sesion_id = cursor.lastrowid
        
        # Insertar 5-8 activos por sesión
        num_activos = random.randint(5, 8)
        for _ in range(num_activos):
            disp = random.choice(DISPOSITIVOS)
            sn = f"{disp['marca'][:2].upper()}{random.randint(100000, 999999)}{random.choice('ABCDEF')}"
            estado = random.choice(ESTADOS)
            origen = random.choice(["ocr", "voz", "manual"])
            
            conn.execute(
                """
                INSERT INTO activos 
                (sesion_id, nombre, marca, modelo, tipo, numero_serie, estado, ubicacion, observaciones, origen, creado_en)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    sesion_id,
                    disp["nombre"],
                    disp["marca"],
                    disp["modelo"],
                    disp["tipo"],
                    sn,
                    estado,
                    f"{pab} - {lab}",
                    "Cargado via seeder",
                    origen,
                    creada_en.strftime("%Y-%m-%d %H:%M:%S")
                )
            )
    
    conn.commit()
    conn.close()
    print("Base de datos poblada con éxito.")

if __name__ == "__main__":
    seed()
