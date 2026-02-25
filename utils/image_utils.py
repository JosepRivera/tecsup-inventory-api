from PIL import Image, ImageEnhance
import io
import base64

MAX_WIDTH = 1600
MAX_HEIGHT = 1600

def preprocesar_imagen(file_bytes: bytes) -> str:
    """
    Mejora contraste y redimensiona la imagen para optimizar el OCR.
    Retorna la imagen como base64 string.
    """
    imagen = Image.open(io.BytesIO(file_bytes)).convert("RGB")

    # Redimensionar si supera el tamaño máximo
    imagen.thumbnail((MAX_WIDTH, MAX_HEIGHT), Image.LANCZOS)

    buffer = io.BytesIO()
    imagen.save(buffer, format="JPEG", quality=90)
    buffer.seek(0)

    return base64.standard_b64encode(buffer.read()).decode("utf-8")


def validar_extension(filename: str) -> bool:
    """Verifica que el archivo sea una imagen soportada."""
    extensiones = {".jpg", ".jpeg", ".png", ".webp", ".heic"}
    suffix = "." + filename.rsplit(".", 1)[-1].lower() if "." in filename else ""
    return suffix in extensiones