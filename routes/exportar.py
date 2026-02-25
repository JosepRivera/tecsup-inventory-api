import os
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from sqlite3 import Connection

from core.dependencies import get_db
from services.pdf_service import generar_pdf_sesion
from services.excel_service import generar_excel_sesion
from services.sesion_service import obtener_sesion_activa
from services.activo_service import listar_activos_sesion

router = APIRouter(prefix="/api/exportar", tags=["Exportar"])


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

    return FileResponse(
        path=ruta,
        media_type="application/pdf",
        filename=os.path.basename(ruta),
    )

@router.get("/excel")
async def exportar_excel(conn: Connection = Depends(get_db)):
    """Genera y descarga el Excel de resumen de la sesión activa."""
    sesion = obtener_sesion_activa(conn)
    if not sesion:
        raise HTTPException(status_code=404, detail="No hay sesión activa.")

    activos = listar_activos_sesion(conn, sesion["id"])
    ruta = generar_excel_sesion(activos, sesion)

    return FileResponse(
        path=ruta,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        filename=os.path.basename(ruta),
    )