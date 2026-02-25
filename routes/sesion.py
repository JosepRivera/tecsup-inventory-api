from fastapi import APIRouter, Depends, HTTPException
from sqlite3 import Connection

from core.dependencies import get_db
from schemas.sesion import SesionCreate, SesionUpdate, SesionResponse
from services.sesion_service import (
    obtener_sesion_activa,
    crear_sesion,
    actualizar_contexto,
    cerrar_sesion,
)

router = APIRouter(prefix="/api/sesion", tags=["Sesion"])


@router.get("/contexto", response_model=SesionResponse)
async def get_contexto(conn: Connection = Depends(get_db)):
    """Retorna el contexto de la sesión activa actual."""
    sesion = obtener_sesion_activa(conn)
    if not sesion:
        raise HTTPException(status_code=404, detail="No hay sesión activa.")
    return SesionResponse(**sesion)


@router.post("/iniciar", response_model=SesionResponse)
async def iniciar_sesion(body: SesionCreate, conn: Connection = Depends(get_db)):
    """Cierra la sesión anterior e inicia una nueva jornada."""
    sesion = crear_sesion(conn, body.pabellon, body.laboratorio, body.armario)
    return SesionResponse(**sesion)


@router.patch("/contexto", response_model=SesionResponse)
async def patch_contexto(body: SesionUpdate, conn: Connection = Depends(get_db)):
    """Actualiza el laboratorio o armario actual sin iniciar nueva sesión."""
    sesion = obtener_sesion_activa(conn)
    if not sesion:
        raise HTTPException(status_code=404, detail="No hay sesión activa.")
    actualizada = actualizar_contexto(
        conn,
        sesion["id"],
        body.pabellon or sesion.get("pabellon"),
        body.laboratorio or sesion.get("laboratorio"),
        body.armario or sesion.get("armario"),
    )
    return SesionResponse(**actualizada)


@router.post("/cerrar")
async def cerrar(conn: Connection = Depends(get_db)):
    """Cierra la sesión activa."""
    sesion = obtener_sesion_activa(conn)
    if not sesion:
        raise HTTPException(status_code=404, detail="No hay sesión activa.")
    cerrar_sesion(conn, sesion["id"])
    return {"mensaje": "Sesión cerrada correctamente."}