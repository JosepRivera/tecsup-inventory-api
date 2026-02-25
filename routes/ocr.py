from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlite3 import Connection

from core.dependencies import get_db
from schemas.ocr import OCRResponse
from schemas.activo import ActivoCreate, ActivoResponse
from services.claude_service import analizar_etiqueta
from services.activo_service import guardar_activo
from services.sesion_service import obtener_sesion_activa
from utils.image_utils import preprocesar_imagen, validar_extension

router = APIRouter(prefix="/api/ocr", tags=["OCR"])


@router.post("/escanear-etiqueta", response_model=OCRResponse)
async def escanear_etiqueta(imagen: UploadFile = File(...)):
    """
    Recibe una foto de etiqueta y devuelve los campos inferidos por Claude Vision.
    El frontend muestra el formulario prellenado para que el técnico confirme.
    """
    if not validar_extension(imagen.filename):
        raise HTTPException(status_code=400, detail="Formato de imagen no soportado.")

    file_bytes = await imagen.read()
    imagen_b64 = preprocesar_imagen(file_bytes)

    try:
        resultado = analizar_etiqueta(imagen_b64)
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Error al procesar con Claude: {str(e)}")

    return OCRResponse(**resultado)


@router.post("/confirmar", response_model=ActivoResponse)
async def confirmar_activo(activo: ActivoCreate, conn: Connection = Depends(get_db)):
    """
    El técnico revisó el formulario prellenado y confirma el guardado.
    Se aplica el contexto de la sesión activa si existe.
    """
    sesion = obtener_sesion_activa(conn)
    datos = activo.model_dump()

    # Aplicar ubicación de la sesión si el activo no tiene una propia
    if sesion and not datos.get("ubicacion"):
        partes = filter(None, [sesion.get("pabellon"), sesion.get("laboratorio"), sesion.get("armario")])
        datos["ubicacion"] = " / ".join(partes)

    if sesion:
        datos["sesion_id"] = sesion["id"]

    datos["origen"] = "ocr"
    guardado = guardar_activo(conn, datos)
    return ActivoResponse(**guardado)