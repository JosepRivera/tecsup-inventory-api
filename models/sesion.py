from dataclasses import dataclass
from typing import Optional

@dataclass
class Sesion:
    id: Optional[int]
    pabellon: Optional[str]
    laboratorio: Optional[str]
    armario: Optional[str]
    activa: int
    creada_en: Optional[str] = None