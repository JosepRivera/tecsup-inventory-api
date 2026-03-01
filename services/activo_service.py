import sqlite3
from typing import Optional, List
from utils.date_utils import get_now_lima_str

def guardar_activo(conn: sqlite3.Connection, datos: dict) -> dict:
    """Inserta un activo en SQLite y retorna el registro creado."""
    cursor = conn.execute(
        """
        INSERT INTO activos
            (sesion_id, nombre, marca, modelo, tipo, numero_serie, estado, ubicacion, observaciones, origen, creado_en)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
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
            get_now_lima_str(),
        ),
    )
    activo_id = cursor.lastrowid
    row = conn.execute("SELECT * FROM activos WHERE id = ?", (activo_id,)).fetchone()
    return dict(row)


def listar_activos_sesion(conn: sqlite3.Connection, sesion_id: int, limit: int = 50, offset: int = 0) -> List[dict]:
    """Retorna los activos registrados en una sesión con paginación, incluyendo el técnico."""
    rows = conn.execute(
        """
        SELECT a.*, s.tecnico
        FROM activos a
        JOIN sesiones s ON a.sesion_id = s.id
        WHERE a.sesion_id = ? 
        ORDER BY a.creado_en DESC 
        LIMIT ? OFFSET ?
        """,
        (sesion_id, limit, offset),
    ).fetchall()
    return [dict(r) for r in rows]


def eliminar_activo(conn: sqlite3.Connection, activo_id: int) -> bool:
    """Elimina un activo por ID (para deshacer el último registro)."""
    conn.execute("DELETE FROM activos WHERE id = ?", (activo_id,))
    return True


def buscar_activos(conn: sqlite3.Connection, query: str, limit: int = 50, offset: int = 0) -> List[dict]:
    """
    Búsqueda local por palabras clave en SQLite con paginación.
    Incluye el nombre del técnico.
    """
    palabras = query.strip().split()
    if not palabras:
        return []

    conditions = []
    params = []
    for palabra in palabras:
        like = f"%{palabra}%"
        conditions.append(
            "(a.nombre LIKE ? OR a.modelo LIKE ? OR a.numero_serie LIKE ? OR a.tipo LIKE ? OR a.marca LIKE ? OR a.ubicacion LIKE ?)"
        )
        params.extend([like, like, like, like, like, like])

    params.extend([limit, offset])
    where_clause = " AND ".join(conditions)
    rows = conn.execute(
        f"""
        SELECT a.*, s.tecnico
        FROM activos a
        JOIN sesiones s ON a.sesion_id = s.id
        WHERE {where_clause}
        ORDER BY a.creado_en DESC
        LIMIT ? OFFSET ?
        """,
        params,
    ).fetchall()
    return [dict(r) for r in rows]


def obtener_activo(conn: sqlite3.Connection, activo_id: int) -> Optional[dict]:
    """Obtiene un activo por su ID incluyendo el técnico."""
    row = conn.execute(
        """
        SELECT a.*, s.tecnico
        FROM activos a
        JOIN sesiones s ON a.sesion_id = s.id
        WHERE a.id = ?
        """, 
        (activo_id,)
    ).fetchone()
    return dict(row) if row else None


def actualizar_activo(conn: sqlite3.Connection, activo_id: int, datos: dict) -> Optional[dict]:
    """Actualiza los campos de un activo."""
    campos_permitidos = ["nombre", "marca", "modelo", "tipo", "numero_serie", "estado", "ubicacion", "observaciones", "origen"]
    update_data = {k: v for k, v in datos.items() if k in campos_permitidos}
    
    if not update_data:
        return obtener_activo(conn, activo_id)

    set_clause = ", ".join([f"{k} = ?" for k in update_data.keys()])
    params = list(update_data.values())
    params.append(activo_id)

    conn.execute(f"UPDATE activos SET {set_clause} WHERE id = ?", params)
    return obtener_activo(conn, activo_id)


def listar_todos_los_activos(conn: sqlite3.Connection, limit: int = 50, offset: int = 0) -> List[dict]:
    """Retorna los activos de todas las sesiones con paginación e información del técnico."""
    rows = conn.execute(
        """
        SELECT a.*, s.tecnico
        FROM activos a
        JOIN sesiones s ON a.sesion_id = s.id
        ORDER BY a.creado_en DESC 
        LIMIT ? OFFSET ?
        """,
        (limit, offset)
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