from pydantic import BaseModel
from typing import Optional

class ActivoBase(BaseModel):
    nombre: Optional[str] = None
    marca: Optional[str] = None
    modelo: Optional[str] = None
    tipo: Optional[str] = None
    numero_serie: Optional[str] = None
    estado: Optional[str] = "Bueno"
    ubicacion: Optional[str] = None
    observaciones: Optional[str] = None

class ActivoCreate(ActivoBase):
    sesion_id: Optional[int] = None
    origen: Optional[str] = "manual"

class ActivoResponse(ActivoBase):
    id: int
    sesion_id: Optional[int]
    origen: Optional[str]
    creado_en: Optional[str]

    class Config:
        from_attributes = True