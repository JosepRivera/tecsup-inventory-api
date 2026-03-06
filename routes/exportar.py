import os
import logging
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from sqlite3 import Connection

from core.dependencies import get_db
from services.pdf_service import generar_pdf_sesion
from services.excel_service import generar_excel_sesion
from services.sesion_service import obtener_sesion_activa
from services.activo_service import listar_activos_sesion, listar_todos_los_activos

logger = logging.getLogger("tecsup-inventory.exportar")
router = APIRouter(prefix="/api/exportar", tags=["Exportar"])


def serve_file(ruta: str, media_type: str):
    """Verifica la existencia del archivo y lo sirve, o lanza 404."""
    if not os.path.exists(ruta):
        logger.error(f"Archivo no encontrado para descarga: {ruta}")
        raise HTTPException(
            status_code=404, 
            detail="El archivo generado no se encuentra en el servidor."
        )
    
    logger.info(f"Sirviendo archivo: {ruta}")
    return FileResponse(
        path=ruta,
        media_type=media_type,
        filename=os.path.basename(ruta),
    )


@router.get("/pdf")
async def exportar_pdf(conn: Connection = Depends(get_db)):
    """
    Genera y descarga el PDF de resumen de la sesión activa.
    """
    sesion = obtener_sesion_activa(conn)
    if not sesion:
        raise HTTPException(status_code=404, detail="No hay sesión activa.")

    activos = listar_activos_sesion(conn, sesion["id"])
    ruta = generar_pdf_sesion(activos, sesion)
    return serve_file(ruta, "application/pdf")

@router.get("/excel")
async def exportar_excel(conn: Connection = Depends(get_db)):
    """Genera y descarga el Excel de resumen de la sesión activa."""
    sesion = obtener_sesion_activa(conn)
    if not sesion:
        raise HTTPException(status_code=404, detail="No hay sesión activa.")

    activos = listar_activos_sesion(conn, sesion["id"])
    ruta = generar_excel_sesion(activos, sesion)
    return serve_file(ruta, "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

@router.get("/global/pdf")
async def exportar_pdf_global(conn: Connection = Depends(get_db)):
    """Genera y descarga el PDF de todo el inventario."""
    activos = listar_todos_los_activos(conn)
    ruta = generar_pdf_sesion(activos, sesion=None)
    return serve_file(ruta, "application/pdf")

@router.get("/global/excel")
async def exportar_excel_global(conn: Connection = Depends(get_db)):
    """Genera y descarga el Excel de todo el inventario."""
    activos = listar_todos_los_activos(conn)
    ruta = generar_excel_sesion(activos, sesion=None)
    return serve_file(ruta, "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")