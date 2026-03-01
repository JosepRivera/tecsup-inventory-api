import sqlite3
from typing import List

def activos_por_tipo(conn: sqlite3.Connection) -> dict:
    """Retorna el conteo de activos agrupado por tipo."""
    rows = conn.execute(
        "SELECT tipo, COUNT(*) as cantidad FROM activos GROUP BY tipo"
    ).fetchall()
    return {r["tipo"] or "Sin tipo": r["cantidad"] for r in rows}


def activos_por_estado(conn: sqlite3.Connection) -> dict:
    """Retorna el conteo de activos agrupado por estado."""
    rows = conn.execute(
        "SELECT estado, COUNT(*) as cantidad FROM activos GROUP BY estado"
    ).fetchall()
    return {r["estado"] or "Sin estado": r["cantidad"] for r in rows}


def activos_por_ubicacion(conn: sqlite3.Connection) -> dict:
    """Retorna el conteo de activos agrupado por ubicación."""
    rows = conn.execute(
        "SELECT ubicacion, COUNT(*) as cantidad FROM activos GROUP BY ubicacion"
    ).fetchall()
    return {r["ubicacion"] or "Sin ubicación": r["cantidad"] for r in rows}


def resumen_general(conn: sqlite3.Connection) -> dict:
    """Retorna un resumen global del inventario."""
    total_activos = conn.execute("SELECT COUNT(*) FROM activos").fetchone()[0]
    total_sesiones = conn.execute("SELECT COUNT(*) FROM sesiones").fetchone()[0]
    
    return {
        "total_activos": total_activos,
        "total_sesiones": total_sesiones,
        "por_tipo": activos_por_tipo(conn),
        "por_estado": activos_por_estado(conn),
    }
