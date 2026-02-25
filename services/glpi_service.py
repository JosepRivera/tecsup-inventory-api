import httpx
import os
from dotenv import load_dotenv
from models.dispositivo import DispositivoGLPI

load_dotenv()

GLPI_URL = os.getenv("GLPI_URL", "")
GLPI_APP_TOKEN = os.getenv("GLPI_APP_TOKEN", "")
GLPI_USER_TOKEN = os.getenv("GLPI_USER_TOKEN", "")


async def obtener_session_token() -> str:
    """
    Inicia sesión en GLPI y obtiene un session token.
    GLPI REST API requiere este token para cada operación.
    """
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{GLPI_URL}/apirest.php/initSession",
            headers={
                "App-Token": GLPI_APP_TOKEN,
                "Authorization": f"user_token {GLPI_USER_TOKEN}",
                "Content-Type": "application/json"
            }
        )
        response.raise_for_status()
        return response.json()["session_token"]


async def cerrar_sesion(session_token: str):
    """Cierra la sesión en GLPI."""
    async with httpx.AsyncClient() as client:
        await client.get(
            f"{GLPI_URL}/apirest.php/killSession",
            headers={
                "App-Token": GLPI_APP_TOKEN,
                "Session-Token": session_token,
            }
        )


async def crear_dispositivo_en_glpi(dispositivo: DispositivoGLPI) -> int:
    """
    Crea un nuevo dispositivo (peripheral) en GLPI.
    Retorna el ID del item creado.

    Referencia API GLPI: POST /apirest.php/Peripheral
    """
    session_token = await obtener_session_token()

    # Mapeo de nuestros campos al formato que espera GLPI
    payload = {
        "input": {
            "name": dispositivo.nombre or "Sin nombre",
            "serial": dispositivo.numero_serial,
            "otherserial": dispositivo.numero_inventario,
            "comment": dispositivo.comentarios,
            # Estos campos en GLPI se manejan por ID, no por nombre
            # Cuando tengan acceso a la API, mapear los IDs correctos
            # "manufacturers_id": ID_DEL_FABRICANTE,
            # "peripheraltypes_id": ID_DEL_TIPO,
            # "locations_id": ID_DE_UBICACION,
            # "states_id": ID_DEL_ESTADO,
        }
    }

    # Limpiar valores None del payload
    payload["input"] = {k: v for k, v in payload["input"].items() if v is not None}

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{GLPI_URL}/apirest.php/Peripheral",
                headers={
                    "App-Token": GLPI_APP_TOKEN,
                    "Session-Token": session_token,
                    "Content-Type": "application/json"
                },
                json=payload
            )
            response.raise_for_status()
            glpi_id = response.json()["id"]
            return glpi_id
    finally:
        await cerrar_sesion(session_token)


async def glpi_disponible() -> bool:
    """Verifica si la API de GLPI está configurada y accesible."""
    if not all([GLPI_URL, GLPI_APP_TOKEN, GLPI_USER_TOKEN]):
        return False
    try:
        await obtener_session_token()
        return True
    except Exception:
        return False