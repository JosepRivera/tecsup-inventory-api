import pytest
import sqlite3
import os
from fastapi.testclient import TestClient
from main import app
from core.dependencies import get_db

# Base de datos de prueba temporal
TEST_DB = "test_inventory.db"

@pytest.fixture(scope="session", autouse=True)
def setup_test_db():
    """Crea las tablas en la base de datos de prueba."""
    conn = sqlite3.connect(TEST_DB, check_same_thread=False)
    # Esquema de tablas (copiado de core/database.py para independencia)
    conn.execute("""
    CREATE TABLE IF NOT EXISTS sesiones (
        id          INTEGER PRIMARY KEY AUTOINCREMENT,
        tecnico     TEXT,
        pabellon    TEXT,
        laboratorio TEXT,
        armario     TEXT,
        activa      INTEGER DEFAULT 1,
        creada_en   DATETIME DEFAULT CURRENT_TIMESTAMP
    );
    """)
    conn.execute("""
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
        origen      TEXT,
        creado_en   DATETIME DEFAULT CURRENT_TIMESTAMP
    );
    """)
    conn.commit()
    conn.close()
    yield
    if os.path.exists(TEST_DB):
        os.remove(TEST_DB)

@pytest.fixture
def db_conn():
    """Provee una conexión a la base de datos de prueba."""
    conn = sqlite3.connect(TEST_DB, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    yield conn
    conn.close()

@pytest.fixture
def client(db_conn):
    """Provee un TestClient de FastAPI con la base de datos de prueba inyectada."""
    def override_get_db():
        yield db_conn
    
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()
