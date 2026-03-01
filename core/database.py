import sqlite3
from contextlib import contextmanager

DB_PATH = "database.db"

CREATE_ACTIVOS = """
CREATE TABLE IF NOT EXISTS activos (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    sesion_id   INTEGER,
    nombre      TEXT,
    marca       TEXT,
    modelo      TEXT,
    tipo        TEXT,
    numero_serie TEXT,
    estado      TEXT DEFAULT 'Bueno',
    ubicacion   TEXT,
    observaciones TEXT,
    origen      TEXT,            -- 'ocr' | 'voz' | 'manual'
    creado_en   DATETIME DEFAULT CURRENT_TIMESTAMP
);
"""

CREATE_SESIONES = """
CREATE TABLE IF NOT EXISTS sesiones (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    tecnico     TEXT,
    pabellon    TEXT,
    laboratorio TEXT,
    armario     TEXT,
    activa      INTEGER DEFAULT 1,   -- 1 = activa, 0 = cerrada
    creada_en   DATETIME DEFAULT CURRENT_TIMESTAMP
);
"""

def init_db():
    """Crea las tablas si no existen al arrancar la app."""
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(CREATE_SESIONES)
        conn.execute(CREATE_ACTIVOS)
        conn.commit()

@contextmanager
def get_connection():
    """Context manager para obtener una conexión con row_factory."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()