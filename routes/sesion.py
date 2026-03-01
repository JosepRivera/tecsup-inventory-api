from fastapi import APIRouter, Depends, HTTPException
from sqlite3 import Connection
from typing import List

from core.dependencies import get_db, get_tecnico
from schemas.sesion import SesionCreate, SesionUpdate, SesionResponse
from services.sesion_service import (
    obtener_sesion_activa,
    crear_sesion,
    actualizar_contexto,
    cerrar_sesion,
    listar_sesiones,
    obtener_sesion_por_id,
)

router = APIRouter(prefix="/api/sesion", tags=["Sesion"])


@router.get("/contexto", response_model=SesionResponse)
async def get_contexto(
    conn: Connection = Depends(get_db), 
    tecnico: str = Depends(get_tecnico)
):
    """Retorna el contexto de la sesión activa actual del técnico."""
    sesion = obtener_sesion_activa(conn, tecnico)
    if not sesion:
        raise HTTPException(status_code=404, detail="No hay sesión activa para este técnico.")
    return SesionResponse(**sesion)


@router.post("/iniciar", response_model=SesionResponse)
async def iniciar_sesion(body: SesionCreate, conn: Connection = Depends(get_db)):
    """Cierra la sesión anterior e inicia una nueva jornada para un técnico."""
    sesion = crear_sesion(conn, body.tecnico, body.pabellon, body.laboratorio, body.armario)
    return SesionResponse(**sesion)


@router.patch("/contexto", response_model=SesionResponse)
async def patch_contexto(
    body: SesionUpdate, 
    conn: Connection = Depends(get_db),
    tecnico: str = Depends(get_tecnico)
):
    """Actualiza el laboratorio o armario actual del técnico."""
    sesion = obtener_sesion_activa(conn, tecnico)
    if not sesion:
        raise HTTPException(status_code=404, detail="No hay sesión activa para este técnico.")
    actualizada = actualizar_contexto(
        conn,
        sesion["id"],
        body.pabellon or sesion.get("pabellon"),
        body.laboratorio or sesion.get("laboratorio"),
        body.armario or sesion.get("armario"),
    )
    return SesionResponse(**actualizada)


@router.post("/cerrar")
async def cerrar(
    conn: Connection = Depends(get_db),
    tecnico: str = Depends(get_tecnico)
):
    """Cierra la sesión activa del técnico."""
    sesion = obtener_sesion_activa(conn, tecnico)
    if not sesion:
        raise HTTPException(status_code=404, detail="No hay sesión activa para este técnico.")
    cerrar_sesion(conn, sesion["id"])
    return {"mensaje": "Sesión cerrada correctamente."}


@router.get("/", response_model=List[SesionResponse])
async def get_sesiones(conn: Connection = Depends(get_db)):
    """Lista todas las sesiones registradas."""
    return [SesionResponse(**s) for s in listar_sesiones(conn)]


@router.get("/{sesion_id}", response_model=SesionResponse)
async def get_sesion(sesion_id: int, conn: Connection = Depends(get_db)):
    """Obtiene una sesión específica."""
    sesion = obtener_sesion_por_id(conn, sesion_id)
    if not sesion:
        raise HTTPException(status_code=404, detail="Sesión no encontrada.")
    return SesionResponse(**sesion)