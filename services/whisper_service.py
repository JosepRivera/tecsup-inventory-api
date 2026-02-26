import httpx
import os
from core.config import settings

GROQ_URL = "https://api.groq.com/openai/v1/audio/transcriptions"

def transcribir(ruta_audio: str) -> str:
    """
    Transcribe el archivo de audio a texto en español usando Groq Whisper API.
    Retorna el texto transcrito.
    """
    with open(ruta_audio, "rb") as f:
        nombre = os.path.basename(ruta_audio)
        respuesta = httpx.post(
            GROQ_URL,
            headers={"Authorization": f"Bearer {settings.GROQ_API_KEY}"},
            files={"file": (nombre, f, "audio/mpeg")},
            data={
                "model": "whisper-large-v3",
                "language": "es",
                "response_format": "json",
            },
            timeout=30.0,
        )

    respuesta.raise_for_status()
    return respuesta.json()["text"].strip()