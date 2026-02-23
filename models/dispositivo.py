from pydantic import BaseModel
from typing import Optional


class DispositivoGLPI(BaseModel):
    """
    Modelo que refleja los campos del formulario de GLPI.
    Todos opcionales porque el OCR puede no detectar todos.
    """
    nombre: Optional[str] = None
    marca: Optional[str] = None
    fabricante: Optional[str] = None
    modelo: Optional[str] = None
    numero_serial: Optional[str] = None
    numero_inventario: Optional[str] = None
    tipo_dispositivo: Optional[str] = None
    ubicacion: Optional[str] = None
    estado: Optional[str] = None
    comentarios: Optional[str] = None
    # Campos extra que el OCR pueda detectar
    otros: Optional[dict] = {}


class RespuestaOCR(BaseModel):
    """Respuesta completa del endpoint de OCR"""
    exito: bool
    dispositivo: Optional[DispositivoGLPI] = None
    texto_completo: Optional[str] = None
    mensaje: Optional[str] = None
    glpi_id: Optional[int] = None  # ID del item creado en GLPI (cuando se integre)