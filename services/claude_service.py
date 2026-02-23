import anthropic
import base64
import json
import re
from PIL import Image, ImageEnhance, ImageFilter, ImageOps
import io
import os
from dotenv import load_dotenv

load_dotenv()

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))


def mejorar_imagen(imagen_bytes: bytes) -> str:
    """
    Preprocesa la imagen para mejorar la lectura OCR.
    Útil para fotos oscuras o con bajo contraste.
    """
    img = Image.open(io.BytesIO(imagen_bytes))

    # Convertir a RGB si es necesario (por si viene PNG con transparencia)
    if img.mode in ("RGBA", "P"):
        img = img.convert("RGB")

    # Escala de grises para mejorar contraste
    img_gris = img.convert("L")

    # Detectar si la imagen es oscura (fondo negro como etiquetas Dell)
    brillo_promedio = sum(img_gris.getdata()) / len(img_gris.getdata())
    if brillo_promedio < 100:
        # Imagen oscura: invertir colores
        img_gris = ImageOps.invert(img_gris)

    # Mejorar contraste y brillo
    img_gris = ImageEnhance.Contrast(img_gris).enhance(2.5)
    img_gris = ImageEnhance.Brightness(img_gris).enhance(1.5)
    img_gris = img_gris.filter(ImageFilter.SHARPEN)

    # Convertir de vuelta a RGB para Claude
    img_final = img_gris.convert("RGB")

    MAX_WIDTH = 1000
    if img_final.width > MAX_WIDTH:
        ratio = MAX_WIDTH / img_final.width
        nueva_altura = int(img_final.height * ratio)
        img_final = img_final.resize((MAX_WIDTH, nueva_altura), Image.LANCZOS)
    
    buffer = io.BytesIO()
    img_final.save(buffer, format="JPEG", quality=95)
    return base64.b64encode(buffer.getvalue()).decode("utf-8")


def extraer_dispositivo_con_claude(imagen_bytes: bytes) -> dict:
    """
    Envía la imagen a Claude Vision y extrae los campos del dispositivo
    estructurados según los campos de GLPI.
    """
    imagen_base64 = mejorar_imagen(imagen_bytes)

    prompt = """Analyze this device label from an educational institution's inventory.

    Extract all visible information and return ONLY a JSON with this exact structure:

    {
    "nombre": "descriptive device name (e.g: Dell Monitor P2222H)",
    "marca": "brand",
    "fabricante": "full manufacturer name",
    "modelo": "exact model",
    "numero_serial": "serial number or service tag",
    "numero_inventario": null,
    "tipo_dispositivo": "type (Monitor, CPU, Keyboard, Mouse, Printer, etc.)",
    "ubicacion": null,
    "estado": "Bueno",
    "comentarios": "any additional relevant info",
    "otros": {
        "express_svc_code": "",
        "input_rating": "",
        "fecha_fabricacion": "",
        "pais_fabricacion": ""
    },
    "texto_completo": "all readable text from the label"
    }

    Rules:
    - Missing fields set to null
    - numero_inventario and ubicacion always null
    - estado default is "Bueno"
    - nombre must be descriptive: "Dell Monitor P2222H" not just "P2222H"
    - Reply ONLY with the JSON, no extra text or code blocks"""

    mensaje = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=1024,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "image",
                        "source": {
                            "type": "base64",
                            "media_type": "image/jpeg",
                            "data": imagen_base64,
                        },
                    },
                    {
                        "type": "text",
                        "text": prompt
                    }
                ],
            }
        ],
    )

    respuesta_texto = mensaje.content[0].text

    # Limpiar bloques markdown si vienen (```json ... ```)
    limpio = re.sub(r"```json|```", "", respuesta_texto).strip()

    return json.loads(limpio)