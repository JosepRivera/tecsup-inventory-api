from fastapi import APIRouter, Depends, HTTPException, Query
from sqlite3 import Connection
from typing import List

from core.dependencies import get_db
from schemas.activo import ActivoResponse, ActivoBase
from services.activo_service import (
    listar_todos_los_activos,
    obtener_activo,
    actualizar_activo,
    eliminar_activo
)

router = APIRouter(prefix="/api/activos", tags=["Activos"])


@router.get("/", response_model=List[ActivoResponse])
async def get_todos_los_activos(
    p: int = Query(1, ge=1),
    size: int = Query(50, ge=1, le=100),
    conn: Connection = Depends(get_db)
):
    """Lista todos los activos registrados históricamente con paginación."""
    offset = (p - 1) * size
    activos = listar_todos_los_activos(conn, limit=size, offset=offset)
    return [ActivoResponse(**a) for a in activos]


@router.get("/{activo_id}", response_model=ActivoResponse)
async def get_activo(activo_id: int, conn: Connection = Depends(get_db)):
    """Obtiene un activo por su ID."""
    activo = obtener_activo(conn, activo_id)
    if not activo:
        raise HTTPException(status_code=404, detail="Activo no encontrado.")
    return ActivoResponse(**activo)


@router.patch("/{activo_id}", response_model=ActivoResponse)
async def update_activo(activo_id: int, body: ActivoBase, conn: Connection = Depends(get_db)):
    """Actualiza la información de un activo."""
    datos = body.model_dump(exclude_unset=True)
    activo = actualizar_activo(conn, activo_id, datos)
    if not activo:
        raise HTTPException(status_code=404, detail="Activo no encontrado.")
    return ActivoResponse(**activo)


@router.delete("/{activo_id}")
async def delete_activo(activo_id: int, conn: Connection = Depends(get_db)):
    """Elimina un activo permanentemente."""
    success = eliminar_activo(conn, activo_id)
    if not success:
        raise HTTPException(status_code=404, detail="Activo no encontrado.")
    return {"mensaje": f"Activo {activo_id} eliminado correctamente."}
