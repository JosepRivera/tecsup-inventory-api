from fastapi import APIRouter, Depends, Query
from sqlite3 import Connection
from typing import List

from core.dependencies import get_db
from schemas.activo import ActivoResponse
from services.activo_service import buscar_activos

router = APIRouter(prefix="/api/busqueda", tags=["Busqueda"])


@router.get("/", response_model=List[ActivoResponse])
async def buscar(q: str = Query(..., min_length=1), conn: Connection = Depends(get_db)):
    """
    Busca activos por número de serie, nombre o modelo.
    Stub listo para conectar con GLPI REST API en el futuro.
    """
    resultados = buscar_activos(conn, q)
    return [ActivoResponse(**r) for r in resultados]