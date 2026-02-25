from dataclasses import dataclass
from typing import Optional

@dataclass
class Activo:
    id: Optional[int]
    sesion_id: Optional[int]
    nombre: Optional[str]
    marca: Optional[str]
    modelo: Optional[str]
    tipo: Optional[str]
    numero_serie: Optional[str]
    estado: str
    ubicacion: Optional[str]
    observaciones: Optional[str]
    origen: Optional[str]
    creado_en: Optional[str] = None