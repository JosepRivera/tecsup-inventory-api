from datetime import datetime
from zoneinfo import ZoneInfo

def get_now_lima() -> datetime:
    """Retorna la fecha y hora actual en la zona horaria de Lima (UTC-5)."""
    return datetime.now(ZoneInfo('America/Lima'))

def get_now_lima_str() -> str:
    """Retorna la fecha y hora actual en Lima como string formateado para SQLite."""
    return get_now_lima().strftime("%Y-%m-%d %H:%M:%S")
