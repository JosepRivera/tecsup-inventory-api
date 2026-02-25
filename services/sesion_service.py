import sqlite3
from typing import Optional

def obtener_sesion_activa(conn: sqlite3.Connection) -> Optional[dict]:
    """Retorna la sesión activa actual o None si no hay ninguna."""
    row = conn.execute(
        "SELECT * FROM sesiones WHERE activa = 1 ORDER BY creada_en DESC LIMIT 1"
    ).fetchone()
    return dict(row) if row else None


def crear_sesion(conn: sqlite3.Connection, pabellon: str, laboratorio: str, armario: str) -> dict:
    """
    Cierra cualquier sesión activa y crea una nueva.
    Retorna la sesión creada.
    """
    conn.execute("UPDATE sesiones SET activa = 0 WHERE activa = 1")
    cursor = conn.execute(
        "INSERT INTO sesiones (pabellon, laboratorio, armario) VALUES (?, ?, ?)",
        (pabellon, laboratorio, armario),
    )
    sesion_id = cursor.lastrowid
    row = conn.execute("SELECT * FROM sesiones WHERE id = ?", (sesion_id,)).fetchone()
    return dict(row)


def actualizar_contexto(conn: sqlite3.Connection, sesion_id: int, pabellon: str, laboratorio: str, armario: str) -> Optional[dict]:
    """Actualiza pabellón, laboratorio y armario de la sesión activa."""
    conn.execute(
        "UPDATE sesiones SET pabellon = ?, laboratorio = ?, armario = ? WHERE id = ?",
        (pabellon, laboratorio, armario, sesion_id),
    )
    row = conn.execute("SELECT * FROM sesiones WHERE id = ?", (sesion_id,)).fetchone()
    return dict(row) if row else None


def cerrar_sesion(conn: sqlite3.Connection, sesion_id: int) -> bool:
    """Marca la sesión como cerrada."""
    conn.execute("UPDATE sesiones SET activa = 0 WHERE id = ?", (sesion_id,))
    return True