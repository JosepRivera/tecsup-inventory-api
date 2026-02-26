import os
from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlite3 import Connection
from typing import List

from core.dependencies import get_db
from schemas.voz import VozResponse
from schemas.activo import ActivoCreate, ActivoResponse
from services.whisper_service import transcribir
from services.claude_service import interpretar_voz
from services.activo_service import guardar_activo, buscar_activos
from services.sesion_service import obtener_sesion_activa
from utils.audio_utils import validar_audio, guardar_temp

router = APIRouter(prefix="/api/voz", tags=["Voz"])


@router.post("/dictar", response_model=VozResponse)
async def dictar(audio: UploadFile = File(...), conn: Connection = Depends(get_db)):
    """
    Recibe un audio, lo transcribe con Whisper y lo interpreta con Claude.
    Si es una consulta, devuelve es_consulta=True con la consulta reformulada.
    """
    if not validar_audio(audio.filename):
        raise HTTPException(status_code=400, detail="Formato de audio no soportado.")

    file_bytes = await audio.read()
    suffix = "." + audio.filename.rsplit(".", 1)[-1].lower()
    ruta_temp = guardar_temp(file_bytes, suffix)

    try:
        transcripcion = transcribir(ruta_temp)
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Error en transcripción: {str(e)}")
    finally:
        os.remove(ruta_temp)

    try:
        resultado = interpretar_voz(transcripcion)
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Error al interpretar con Claude: {str(e)}")

    # Si Claude detecta que es una consulta, ejecutamos la búsqueda directamente
    if resultado.get("es_consulta"):
        # Preferir un query específico si Claude lo proporciona
        query = (
            resultado.get("query_busqueda")
            or resultado.get("numero_serie")
            or resultado.get("modelo")
            or resultado.get("nombre")
            or resultado.get("respuesta_consulta")
            or transcripcion
        )
        encontrados = buscar_activos(conn, query)
        resultado["resultados"] = [ActivoResponse(**r) for r in encontrados]

    resultado["transcripcion"] = transcripcion
    return VozResponse(**resultado)


@router.post("/confirmar", response_model=ActivoResponse)
async def confirmar_voz(activo: ActivoCreate, conn: Connection = Depends(get_db)):
    """
    El técnico confirma el activo dictado por voz para guardarlo.
    """
    sesion = obtener_sesion_activa(conn)
    datos = activo.model_dump()

    if sesion and not datos.get("ubicacion"):
        partes = filter(None, [sesion.get("pabellon"), sesion.get("laboratorio"), sesion.get("armario")])
        datos["ubicacion"] = " / ".join(partes)

    if sesion:
        datos["sesion_id"] = sesion["id"]

    datos["origen"] = "voz"
    guardado = guardar_activo(conn, datos)
    return ActivoResponse(**guardado)