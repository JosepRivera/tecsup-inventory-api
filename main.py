from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from core.config import settings
from core.database import init_db
from routes import ocr, voz, sesion, dashboard, busqueda, exportar

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
)

# CORS abierto en desarrollo
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(ocr.router)
app.include_router(voz.router)
app.include_router(sesion.router)
app.include_router(dashboard.router)
app.include_router(busqueda.router)
app.include_router(exportar.router)

@app.get("/")
def root():
    return {"estado": "ok", "ambiente": settings.APP_ENV}