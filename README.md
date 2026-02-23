<div align="center">

# Tecsup Inventory API

[![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688?style=for-the-badge&logo=fastapi&logoColor=white&labelColor=009688&color=2d2d2d)](https://fastapi.tiangolo.com/)
[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white&labelColor=3776AB&color=2d2d2d)](https://www.python.org/)
[![Anthropic](https://img.shields.io/badge/Claude_Vision-Haiku-CC785C?style=for-the-badge&logoColor=white&labelColor=CC785C&color=2d2d2d)](https://www.anthropic.com/)
[![GLPI](https://img.shields.io/badge/GLPI-REST_API-FF6900?style=for-the-badge&logoColor=white&labelColor=FF6900&color=2d2d2d)](https://glpi-project.org/)
[![MIT License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge&logo=opensourceinitiative&logoColor=white&labelColor=yellow&color=2d2d2d)](./LICENSE)

**REST API para inventariado inteligente de dispositivos tecnológicos.**  
Escanea etiquetas con la cámara del celular y registra automáticamente en GLPI.

</div>

---

## Tabla de Contenidos

- [Tecsup Inventory API](#tecsup-inventory-api)
  - [Tabla de Contenidos](#tabla-de-contenidos)
  - [Descripción](#descripción)
  - [Tech Stack](#tech-stack)
  - [Funcionalidades](#funcionalidades)
  - [Arquitectura del Proyecto](#arquitectura-del-proyecto)
  - [Variables de Entorno](#variables-de-entorno)
  - [Instalación y Setup](#instalación-y-setup)
    - [Prerrequisitos](#prerrequisitos)
    - [Pasos](#pasos)
  - [Comandos Disponibles](#comandos-disponibles)
  - [Documentación API](#documentación-api)
    - [Endpoint principal](#endpoint-principal)
  - [Licencia](#licencia)

---

## Descripción

**Tecsup Inventory API** es el backend de un sistema de inventariado de dispositivos tecnológicos desarrollado como proyecto de pasantía en **Tecsup**.

El problema que resuelve: inventariar manualmente ~5000 equipos distribuidos en más de 20 laboratorios es un proceso lento y propenso a errores. Esta API permite que un técnico tome una foto de la etiqueta de cualquier dispositivo con su celular y obtenga automáticamente los datos estructurados (marca, modelo, número de serie, etc.) listos para registrar en el sistema GLPI del instituto.

Construida con **FastAPI** y **Claude Vision (Haiku)**, procesa imágenes en tiempo real con alta precisión incluso en condiciones de poca iluminación.

---

## Tech Stack

**Core**

![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=flat-square&logo=fastapi&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white)

**IA & OCR**

![Anthropic](https://img.shields.io/badge/Claude_Vision-CC785C?style=flat-square&logoColor=white)
![Pillow](https://img.shields.io/badge/Pillow-3776AB?style=flat-square&logo=python&logoColor=white)

**Integración**

![GLPI](https://img.shields.io/badge/GLPI_REST_API-FF6900?style=flat-square&logoColor=white)
![HTTPX](https://img.shields.io/badge/HTTPX-009688?style=flat-square&logoColor=white)

---

## Funcionalidades

| Módulo | Estado |
| --- | --- |
| **OCR de etiquetas** — Foto de etiqueta → JSON estructurado con Claude Vision | ✅ Listo |
| **Preprocesamiento de imagen** — Mejora automática de brillo/contraste para fotos oscuras | ✅ Listo |
| **Integración GLPI** — Registro automático del dispositivo en GLPI via REST API | 🚧 En progreso |
| **Dictado de voz** — Audio del técnico → JSON de inventario con Whisper + Claude | 📋 Planificado |

---

## Arquitectura del Proyecto

```
tecsup-inventory-api/
├── main.py                  # Entrada de la app, configuración CORS
├── routes/
│   ├── __init__.py
│   └── ocr.py               # Endpoint POST /api/ocr/escanear-etiqueta
├── services/
│   ├── __init__.py
│   ├── claude_service.py    # Lógica OCR con Claude Vision
│   └── glpi_service.py      # Integración con GLPI REST API
├── models/
│   ├── __init__.py
│   └── dispositivo.py       # Modelos Pydantic (campos del formulario GLPI)
├── requirements.txt
├── .env.example
└── README.md
```

---

## Variables de Entorno

Copia el archivo de ejemplo antes de iniciar:

```bash
cp .env.example .env
```

| Variable | Descripción | Ejemplo |
| --- | --- | --- |
| `ANTHROPIC_API_KEY` | API Key de Anthropic (Claude Vision) | `sk-ant-...` |
| `GLPI_URL` | URL base del GLPI del instituto | `https://glpi.appstecsup.com` |
| `GLPI_APP_TOKEN` | App Token de la API REST de GLPI | — |
| `GLPI_USER_TOKEN` | User Token de la API REST de GLPI | — |

> **Nunca** subas tu archivo `.env` al repositorio. Está incluido en `.gitignore`.

---

## Instalación y Setup

### Prerrequisitos

- Python 3.11+
- pip o cualquier gestor de paquetes Python

### Pasos

**1. Clonar el repositorio**

```bash
git clone https://github.com/JosepRivera/tecsup-inventory-api.git
cd tecsup-inventory-api
```

**2. Crear entorno virtual**

```bash
python -m venv .venv
source .venv/bin/activate        # Linux / Mac
.venv\Scripts\activate           # Windows
```

**3. Instalar dependencias**

```bash
pip install -r requirements.txt
```

**4. Configurar variables de entorno**

```bash
cp .env.example .env
# Edita .env y agrega tu API Key de Anthropic
```

**5. Levantar el servidor**

```bash
uvicorn main:app --reload
```

La API estará disponible en `http://localhost:8000`.

---

## Comandos Disponibles

| Comando | Descripción |
| --- | --- |
| `uvicorn main:app --reload` | Inicia el servidor en modo desarrollo con hot-reload |
| `uvicorn main:app --host 0.0.0.0 --port 8000` | Inicia el servidor accesible desde la red local (para la app móvil) |

---

## Documentación API

Una vez levantado el servidor, la documentación interactiva estará disponible en:

```
http://localhost:8000/docs
```

### Endpoint principal

```
POST /api/ocr/escanear-etiqueta
```

Recibe una foto de etiqueta y devuelve los datos del dispositivo en JSON:

```json
{
  "exito": true,
  "dispositivo": {
    "nombre": "Monitor Dell P2222H",
    "marca": "DELL",
    "fabricante": "Dell",
    "modelo": "P2222H",
    "numero_serial": "5KRG2P3",
    "tipo_dispositivo": "Monitor",
    "estado": "Bueno",
    "otros": {
      "express_svc_code": "12139334823",
      "input_rating": "100-240V ~ 50/60Hz 1.5A",
      "fecha_fabricacion": "Mar 2023",
      "pais_fabricacion": "China"
    }
  },
  "mensaje": "Etiqueta escaneada correctamente"
}
```

Agrega `?guardar_en_glpi=true` para registrar automáticamente en GLPI (requiere credenciales configuradas).

---

## Licencia

Este proyecto está bajo la licencia **MIT**.