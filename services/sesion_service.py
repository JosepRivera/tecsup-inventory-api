import sqlite3
import re
from typing import Optional
from utils.date_utils import get_now_lima_str

def normalizar_texto(texto: str) -> str:
    """
    Normaliza el texto: quita espacios extra, capitaliza correctamente
    y asegura un formato estándar para Laboratorios y Pabellones.
    Ej: "laboratorio3" -> "Laboratorio 3"
    """
    if not texto:
        return ""
    
    # Limpieza básica
    t = texto.strip()
    
    # Si es "labX" o "laboratorioX", convertir a "Laboratorio X"
    match_lab = re.match(r"^(lab(oratorio)?)\s*(\d+)$", t, re.IGNORECASE)
    if match_lab:
        return f"Laboratorio {match_lab.group(3)}"
        
    # Si es "pabellonX", "pabellon X", "pab X", convertir a "Pabellón X"
    match_pab = re.match(r"^(pab(ell[oó]n)?)\s*([a-z0-9]+)$", t, re.IGNORECASE)
    if match_pab:
        return f"Pabellón {match_pab.group(3).upper()}"

    # Default: title case y sin espacios múltiples
    return " ".join(t.split()).title()

def obtener_sesion_activa(conn: sqlite3.Connection, tecnico: Optional[str] = None) -> Optional[dict]:
    """Retorna la sesión activa actualmente. Si se pasa tecnico, busca la de ese técnico."""
    if tecnico:
        t = normalizar_texto(tecnico)
        query = "SELECT * FROM sesiones WHERE activa = 1 AND tecnico = ? ORDER BY creada_en DESC LIMIT 1"
        row = conn.execute(query, (t,)).fetchone()
        if row:
            return dict(row)
    
    # Fallback: si no hay técnico o no se encontró sesión específica, 
    # buscamos la última sesión activa global (para evitar bloqueos)
    row = conn.execute(
        "SELECT * FROM sesiones WHERE activa = 1 ORDER BY creada_en DESC LIMIT 1"
    ).fetchone()
    return dict(row) if row else None


def crear_sesion(conn: sqlite3.Connection, tecnico: str, pabellon: str, laboratorio: str, armario: str) -> dict:
    """
    Cierra cualquier sesión activa DEL TÉCNICO y crea una nueva con datos normalizados.
    """
    t = normalizar_texto(tecnico)
    p = normalizar_texto(pabellon)
    l = normalizar_texto(laboratorio)
    a = normalizar_texto(armario)

    # Solo desactivar las sesiones de ESTE técnico
    conn.execute("UPDATE sesiones SET activa = 0 WHERE activa = 1 AND tecnico = ?", (t,))
    
    now = get_now_lima_str()
    cursor = conn.execute(
        "INSERT INTO sesiones (tecnico, pabellon, laboratorio, armario, creada_en) VALUES (?, ?, ?, ?, ?)",
        (t, p, l, a, now),
    )
    sesion_id = cursor.lastrowid
    row = conn.execute("SELECT * FROM sesiones WHERE id = ?", (sesion_id,)).fetchone()
    return dict(row)


def actualizar_contexto(conn: sqlite3.Connection, sesion_id: int, pabellon: str, laboratorio: str, armario: str) -> Optional[dict]:
    """Actualiza pabellón, laboratorio y armario de la sesión activa con normalización."""
    p = normalizar_texto(pabellon)
    l = normalizar_texto(laboratorio)
    a = normalizar_texto(armario)

    conn.execute(
        "UPDATE sesiones SET pabellon = ?, laboratorio = ?, armario = ? WHERE id = ?",
        (p, l, a, sesion_id),
    )
    row = conn.execute("SELECT * FROM sesiones WHERE id = ?", (sesion_id,)).fetchone()
    return dict(row) if row else None


def cerrar_sesion(conn: sqlite3.Connection, sesion_id: int) -> bool:
    """Marca la sesión como cerrada."""
    conn.execute("UPDATE sesiones SET activa = 0 WHERE id = ?", (sesion_id,))
    return True


def listar_sesiones(conn: sqlite3.Connection) -> list:
    """Retorna todas las sesiones registradas."""
    rows = conn.execute("SELECT * FROM sesiones ORDER BY creada_en DESC").fetchall()
    return [dict(r) for r in rows]


def obtener_sesion_por_id(conn: sqlite3.Connection, sesion_id: int) -> Optional[dict]:
    """Obtiene una sesión específica por su ID."""
    row = conn.execute("SELECT * FROM sesiones WHERE id = ?", (sesion_id,)).fetchone()
    return dict(row) if row else None