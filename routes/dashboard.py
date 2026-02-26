from fastapi import APIRouter, Depends, HTTPException
from sqlite3 import Connection
from typing import List

from core.dependencies import get_db
from schemas.activo import ActivoResponse
from services.sesion_service import obtener_sesion_activa
from services.activo_service import listar_activos_sesion, eliminar_activo, resumen_activos_sesion

router = APIRouter(prefix="/api/dashboard", tags=["Dashboard"])


@router.get("/activos", response_model=List[ActivoResponse])
async def get_activos_sesion(conn: Connection = Depends(get_db)):
    """Lista todos los activos registrados en la sesión activa."""
    sesion = obtener_sesion_activa(conn)
    if not sesion:
        raise HTTPException(status_code=404, detail="No hay sesión activa.")
    activos = listar_activos_sesion(conn, sesion["id"])
    return [ActivoResponse(**a) for a in activos]


@router.delete("/activos/{activo_id}")
async def deshacer_activo(activo_id: int, conn: Connection = Depends(get_db)):
    """Elimina un activo registrado en la sesión (deshacer)."""
    eliminar_activo(conn, activo_id)
    return {"mensaje": f"Activo {activo_id} eliminado."}


@router.get("/resumen")
async def get_resumen_sesion(conn: Connection = Depends(get_db)):
    """
    Devuelve un resumen de la sesión activa:
    - total de activos registrados
    - conteo por origen (ocr, voz, manual).
    """
    sesion = obtener_sesion_activa(conn)
    if not sesion:
        raise HTTPException(status_code=404, detail="No hay sesión activa.")

    return resumen_activos_sesion(conn, sesion["id"])