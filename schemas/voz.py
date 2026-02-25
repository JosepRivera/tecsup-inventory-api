from pydantic import BaseModel
from typing import Optional

class VozResponse(BaseModel):
    transcripcion: Optional[str] = None
    nombre: Optional[str] = None
    marca: Optional[str] = None
    modelo: Optional[str] = None
    tipo: Optional[str] = None
    numero_serie: Optional[str] = None
    estado: Optional[str] = None
    ubicacion: Optional[str] = None
    observaciones: Optional[str] = None
    es_consulta: bool = False           # True si el técnico preguntó algo en vez de dictar
    respuesta_consulta: Optional[str] = None