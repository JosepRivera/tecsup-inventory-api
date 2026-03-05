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

# Usar gunicorn como gestor de procesos (requiere pip install gunicorn)
exec gunicorn main:app \
    --workers $WORKERS \
    --worker-class uvicorn.workers.UvicornWorker \
    --bind $HOST:$PORT \
    --access-logfile - \
    --error-logfile -
