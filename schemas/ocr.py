from pydantic import BaseModel
from typing import Optional

class OCRResponse(BaseModel):
    nombre: Optional[str] = None
    marca: Optional[str] = None
    modelo: Optional[str] = None
    tipo: Optional[str] = None
    numero_serie: Optional[str] = None
    observaciones: Optional[str] = None
    confianza: Optional[str] = None    # 'alta' | 'media' | 'baja'
    texto_raw: Optional[str] = None    # texto completo detectado como fallback