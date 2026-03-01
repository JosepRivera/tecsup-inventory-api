from fastapi import APIRouter, Depends, HTTPException
from sqlite3 import Connection
from typing import List

from core.dependencies import get_db, get_tecnico
from schemas.activo import ActivoResponse
from services.sesion_service import obtener_sesion_activa
from services.activo_service import listar_activos_sesion, eliminar_activo, resumen_activos_sesion
from services import estadistica_service

router = APIRouter(prefix="/api/dashboard", tags=["Dashboard"])


@router.get("/activos", response_model=List[ActivoResponse])
async def get_activos_sesion(
    conn: Connection = Depends(get_db),
    tecnico: str = Depends(get_tecnico)
):
    """Lista todos los activos registrados en la sesión activa del técnico."""
    sesion = obtener_sesion_activa(conn, tecnico)
    if not sesion:
        raise HTTPException(status_code=404, detail="No hay sesión activa para este técnico.")
    activos = listar_activos_sesion(conn, sesion["id"])
    return [ActivoResponse(**a) for a in activos]


@router.delete("/activos/{activo_id}")
async def deshacer_activo(activo_id: int, conn: Connection = Depends(get_db)):
    """Elimina un activo registrado en la sesión (deshacer)."""
    eliminar_activo(conn, activo_id)
    return {"mensaje": f"Activo {activo_id} eliminado."}


@router.get("/resumen")
async def get_resumen_sesion(
    conn: Connection = Depends(get_db),
    tecnico: str = Depends(get_tecnico)
):
    """
    Devuelve un resumen de la sesión activa del técnico:
    - total de activos registrados
    - conteo por origen (ocr, voz, manual).
    """
    sesion = obtener_sesion_activa(conn, tecnico)
    if not sesion:
        raise HTTPException(status_code=404, detail="No hay sesión activa para este técnico.")

    return resumen_activos_sesion(conn, sesion["id"])


@router.get("/estadisticas/global")
async def get_estadisticas_global(conn: Connection = Depends(get_db)):
    """Retorna estadísticas globales del inventario."""
    return estadistica_service.resumen_general(conn)


@router.get("/estadisticas/tipo")
async def get_estadisticas_tipo(conn: Connection = Depends(get_db)):
    """Retorna activos agrupados por tipo."""
    return estadistica_service.activos_por_tipo(conn)


@router.get("/estadisticas/estado")
async def get_estadisticas_estado(conn: Connection = Depends(get_db)):
    """Retorna activos agrupados por estado."""
    return estadistica_service.activos_por_estado(conn)