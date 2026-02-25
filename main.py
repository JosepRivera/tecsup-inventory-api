from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from core.config import settings
from core.database import init_db
from routes import ocr, voz, sesion, dashboard, busqueda, exportar

app = FastAPI(
    title="GLPI Inventario Móvil",
    description="API para inventariado de dispositivos con OCR y voz.",
    version="1.0.0",
)

# CORS abierto en desarrollo para que el celular pueda conectarse por IP local
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inicializar base de datos al arrancar
@app.on_event("startup")
def startup():
    init_db()

# Registro de routers
app.include_router(ocr.router)
app.include_router(voz.router)
app.include_router(sesion.router)
app.include_router(dashboard.router)
app.include_router(busqueda.router)
app.include_router(exportar.router)


@app.get("/")
def root():
    return {"estado": "ok", "ambiente": settings.APP_ENV}