#!/bin/bash
# Script para iniciar la API en producción

# Activar entorno virtual si existe
if [ -d ".venv" ]; then
    source .venv/bin/activate
fi

# Parámetros producción
HOST=${APP_HOST:-0.0.0.0}
PORT=${APP_PORT:-8000}
WORKERS=4

echo "Iniciando Tecsup Inventory API en modo PRODUCCIÓN..."
echo "Host: $HOST | Port: $PORT | Workers: $WORKERS"

# Ejecutar seeder si se solicita vía variable de entorno
if [ "$RUN_SEEDER" = "true" ]; then
    echo "Ejecutando seeder de base de datos..."
    python scripts/seed_db.py
fi

# Usar gunicorn como gestor de procesos (requiere pip install gunicorn)
exec gunicorn main:app \
    --workers $WORKERS \
    --worker-class uvicorn.workers.UvicornWorker \
    --bind $HOST:$PORT \
    --access-logfile - \
    --error-logfile -
