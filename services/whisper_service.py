import whisper
import os

# Carga el modelo una sola vez al importar el módulo
_modelo = whisper.load_model("tiny")

def transcribir(ruta_audio: str) -> str:
    """
    Transcribe el archivo de audio a texto en español.
    Retorna el texto transcrito.
    """
    resultado = _modelo.transcribe(ruta_audio, language="es")
    return resultado["text"].strip()