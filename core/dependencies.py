from core.database import get_connection

async def get_db():
    """Dependencia de FastAPI: provee conexión a SQLite por request."""
    with get_connection() as conn:
        yield conn