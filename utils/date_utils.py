from datetime import datetime
import pytz

def get_now_lima() -> datetime:
    """Retorna la fecha y hora actual en la zona horaria de Lima (UTC-5)."""
    lima_tz = pytz.timezone('America/Lima')
    return datetime.now(lima_tz)

def get_now_lima_str() -> str:
    """Retorna la fecha y hora actual en Lima como string formateado para SQLite."""
    return get_now_lima().strftime("%Y-%m-%d %H:%M:%S")
