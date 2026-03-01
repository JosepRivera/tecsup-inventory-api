from fastapi import APIRouter, Depends, Query
from sqlite3 import Connection
from typing import List

from core.dependencies import get_db
from schemas.activo import ActivoResponse
from services.activo_service import buscar_activos

router = APIRouter(prefix="/api/busqueda", tags=["Busqueda"])


@router.get("/", response_model=List[ActivoResponse])
async def buscar(
    q: str = Query(..., min_length=1),
    p: int = Query(1, ge=1),
    size: int = Query(50, ge=1, le=100),
    conn: Connection = Depends(get_db)
):
    """
    Busca activos por número de serie, nombre o modelo en la base local (SQLite) con paginación.
    """
    offset = (p - 1) * size
    resultados = buscar_activos(conn, q, limit=size, offset=offset)
    return [ActivoResponse(**r) for r in resultados]