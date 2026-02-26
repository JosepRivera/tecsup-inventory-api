import sqlite3
from typing import Optional, List

def guardar_activo(conn: sqlite3.Connection, datos: dict) -> dict:
    """Inserta un activo en SQLite y retorna el registro creado."""
    cursor = conn.execute(
        """
        INSERT INTO activos
            (sesion_id, nombre, marca, modelo, tipo, numero_serie, estado, ubicacion, observaciones, origen)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            datos.get("sesion_id"),
            datos.get("nombre"),
            datos.get("marca"),
            datos.get("modelo"),
            datos.get("tipo"),
            datos.get("numero_serie"),
            datos.get("estado", "Bueno"),
            datos.get("ubicacion"),
            datos.get("observaciones"),
            datos.get("origen", "manual"),
        ),
    )
    activo_id = cursor.lastrowid
    row = conn.execute("SELECT * FROM activos WHERE id = ?", (activo_id,)).fetchone()
    return dict(row)


def listar_activos_sesion(conn: sqlite3.Connection, sesion_id: int) -> List[dict]:
    """Retorna todos los activos registrados en una sesión."""
    rows = conn.execute(
        "SELECT * FROM activos WHERE sesion_id = ? ORDER BY creado_en DESC",
        (sesion_id,),
    ).fetchall()
    return [dict(r) for r in rows]


def eliminar_activo(conn: sqlite3.Connection, activo_id: int) -> bool:
    """Elimina un activo por ID (para deshacer el último registro)."""
    conn.execute("DELETE FROM activos WHERE id = ?", (activo_id,))
    return True


def buscar_activos(conn: sqlite3.Connection, query: str) -> List[dict]:
    """
    Búsqueda local por número de serie, nombre o modelo en SQLite.
    """
    like = f"%{query}%"
    rows = conn.execute(
        """
        SELECT * FROM activos
        WHERE numero_serie LIKE ?
           OR nombre LIKE ?
           OR modelo LIKE ?
        ORDER BY creado_en DESC
        """,
        (like, like, like),
    ).fetchall()
    return [dict(r) for r in rows]


def resumen_activos_sesion(conn: sqlite3.Connection, sesion_id: int) -> dict:
    """
    Devuelve un resumen de la sesión: total de activos y conteo por origen.
    """
    rows = conn.execute(
        """
        SELECT origen, COUNT(*) as cantidad
        FROM activos
        WHERE sesion_id = ?
        GROUP BY origen
        """,
        (sesion_id,),
    ).fetchall()

    total = sum(r["cantidad"] for r in rows)
    por_origen = {r["origen"] or "desconocido": r["cantidad"] for r in rows}

    return {
        "total": total,
        "por_origen": por_origen,
    }