import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from core.config import settings
from core.database import init_db
from routes import ocr, voz, sesion, dashboard, busqueda, exportar, activos

# Configuración básica de logging
logging.basicConfig(
    level=logging.INFO if settings.APP_ENV == "production" else logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger("tecsup-inventory")

@asynccontextmanager
async def lifespan(_: FastAPI):
    # Código que se ejecuta antes de aceptar peticiones
    init_db()
    yield


app = FastAPI(
    title="Tecsup Inventory API",
    description="API para inventariado de dispositivos con OCR y voz.",
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs" if settings.APP_ENV != "production" else None,
    redoc_url="/redoc" if settings.APP_ENV != "production" else None,
)

# CORS dinámico según ambiente
origins = ["*"] if settings.APP_ENV != "production" else [
    "https://tu-frontend-produccion.com", # Reemplazar con URL real
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*", "X-Tecnico"],
)

# Manejador global de errores para producción
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Error no manejado en {request.url}: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"detail": "Error interno del servidor. Por favor, contacte al administrador."},
    )

# Routers
app.include_router(ocr.router)
app.include_router(voz.router)
app.include_router(sesion.router)
app.include_router(dashboard.router)
app.include_router(busqueda.router)
app.include_router(exportar.router)
app.include_router(activos.router)

@app.get("/")
def root():
    return {"estado": "ok", "ambiente": settings.APP_ENV}