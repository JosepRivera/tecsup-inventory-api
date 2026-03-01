from pydantic import BaseModel
from typing import Optional

class SesionCreate(BaseModel):
    tecnico: str
    pabellon: Optional[str] = None
    laboratorio: Optional[str] = None
    armario: Optional[str] = None

class SesionUpdate(BaseModel):
    tecnico: Optional[str] = None
    pabellon: Optional[str] = None
    laboratorio: Optional[str] = None
    armario: Optional[str] = None

class SesionResponse(BaseModel):
    id: int
    pabellon: Optional[str]
    laboratorio: Optional[str]
    armario: Optional[str]
    activa: int
    creada_en: Optional[str]