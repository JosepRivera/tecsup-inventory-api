import json
import anthropic
from core.config import settings
from prompts.ocr_prompt import OCR_SYSTEM, OCR_USER
from prompts.voz_prompt import VOZ_SYSTEM, VOZ_USER_TEMPLATE

client = anthropic.Anthropic(api_key=settings.ANTHROPIC_API_KEY)

MODEL = "claude-haiku-4-5"


def analizar_etiqueta(imagen_base64: str) -> dict:
    """
    Envía la imagen a Claude Vision y retorna los campos del formulario.
    Lanza excepción si la respuesta no es JSON parseable.
    """
    mensaje = client.messages.create(
        model=MODEL,
        max_tokens=512,
        system=OCR_SYSTEM,
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
                    {"type": "text", "text": OCR_USER},
                ],
            }
        ],
    )

    texto = mensaje.content[0].text.strip()

    # Limpiar markdown si Claude lo añade por error
    if texto.startswith("```"):
        texto = texto.split("```")[1]
        if texto.startswith("json"):
            texto = texto[4:]

    return json.loads(texto)


def interpretar_voz(transcripcion: str) -> dict:
    """
    Envía la transcripción a Claude y retorna los campos estructurados.
    Lanza excepción si la respuesta no es JSON parseable.
    """
    prompt = VOZ_USER_TEMPLATE.format(transcripcion=transcripcion)

    mensaje = client.messages.create(
        model=MODEL,
        max_tokens=512,
        system=VOZ_SYSTEM,
        messages=[{"role": "user", "content": prompt}],
    )

    texto = mensaje.content[0].text.strip()

    if texto.startswith("```"):
        texto = texto.split("```")[1]
        if texto.startswith("json"):
            texto = texto[4:]

    return json.loads(texto)