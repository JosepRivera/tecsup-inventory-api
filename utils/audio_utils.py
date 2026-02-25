import os
import tempfile

FORMATOS_SOPORTADOS = {".mp3", ".mp4", ".wav", ".m4a", ".ogg", ".webm"}

def validar_audio(filename: str) -> bool:
    """Verifica que el archivo sea un formato de audio soportado."""
    suffix = "." + filename.rsplit(".", 1)[-1].lower() if "." in filename else ""
    return suffix in FORMATOS_SOPORTADOS


def guardar_temp(file_bytes: bytes, suffix: str) -> str:
    """
    Guarda el audio en un archivo temporal y retorna la ruta.
    El llamador es responsable de eliminar el archivo después de usarlo.
    """
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=suffix)
    tmp.write(file_bytes)
    tmp.close()
    return tmp.name