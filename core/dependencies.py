from fastapi import Header
from core.database import get_connection

async def get_db():
    """Dependencia de FastAPI: provee conexión a SQLite por request."""
    with get_connection() as conn:
        yield conn

async def get_tecnico(x_tecnico: str = Header(None, alias="X-Tecnico")):
    """Identifica al técnico desde el header personalizado."""
    return x_tecnico
