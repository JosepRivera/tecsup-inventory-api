from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.ocr import router as ocr_router

app = FastAPI(
    title="Inventario Tecsup API",
    description="API para escanear etiquetas de dispositivos y registrar inventario en GLPI",
    version="1.0.0",
)

# CORS: permite que la app móvil se conecte
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción cambiar por la IP de la app
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Rutas
app.include_router(ocr_router)


@app.get("/")
async def root():
    return {
        "proyecto": "Inventario Tecsup",
        "version": "1.0.0",
        "docs": "/docs",
        "endpoints": {
            "ocr": "/api/ocr/escanear-etiqueta",
            "health": "/api/ocr/health"
        }
    }