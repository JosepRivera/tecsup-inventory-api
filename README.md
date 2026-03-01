<div align="center">

# Tecsup Inventory API

[![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688?style=for-the-badge&logo=fastapi&logoColor=white&labelColor=009688&color=2d2d2d)](https://fastapi.tiangolo.com/)
[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white&labelColor=3776AB&color=2d2d2d)](https://www.python.org/)
[![Anthropic](https://img.shields.io/badge/Claude_Vision-Haiku-CC785C?style=for-the-badge&logoColor=white&labelColor=CC785C&color=2d2d2d)](https://www.anthropic.com/)
[![Groq](https://img.shields.io/badge/Groq-Whisper-F55036?style=for-the-badge&logoColor=white&labelColor=F55036&color=2d2d2d)](https://console.groq.com/)
[![MIT License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge&logo=opensourceinitiative&logoColor=white&labelColor=yellow&color=2d2d2d)](./LICENSE)

**REST API para inventariado inteligente de dispositivos tecnológicos.**  
Escanea etiquetas con la cámara del celular y registra en el sistema con IA.

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
    - [Endpoints principales](#endpoints-principales)
      - [OCR de etiquetas](#ocr-de-etiquetas)
      - [Dictado de voz](#dictado-de-voz)
      - [Sesión](#sesión)
      - [Dashboard](#dashboard)
      - [Búsqueda](#búsqueda)
      - [Exportación](#exportación)
  - [Licencia](#licencia)

---

## Descripción

**Tecsup Inventory API** es el backend de un sistema de inventariado de dispositivos tecnológicos desarrollado como proyecto de pasantía en **Tecsup**.

El problema que resuelve: inventariar manualmente ~5000 equipos distribuidos en más de 20 laboratorios es un proceso lento y propenso a errores. Esta API permite que un técnico tome una foto de la etiqueta de cualquier dispositivo con su celular y obtenga automáticamente los datos estructurados (marca, modelo, número de serie, etc.) listos para registrar en el sistema. Alternativamente, puede dictar la información por voz y el sistema la interpreta y estructura automáticamente.

Construida con **FastAPI**, **Claude Vision (Haiku)** y **Groq Whisper API**, procesa imágenes y audio en tiempo real con alta precisión incluso en condiciones de poca iluminación.

---

## Tech Stack

**Core**

![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=flat-square&logo=fastapi&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-003B57?style=flat-square&logo=sqlite&logoColor=white)

**IA & OCR**

![Anthropic](https://img.shields.io/badge/Claude_Vision_Haiku-CC785C?style=flat-square&logoColor=white)
![Groq](https://img.shields.io/badge/Groq_Whisper_API-F55036?style=flat-square&logoColor=white)
![Pillow](https://img.shields.io/badge/Pillow-3776AB?style=flat-square&logo=python&logoColor=white)

**Exportación**

![ReportLab](https://img.shields.io/badge/ReportLab-PDF-red?style=flat-square&logoColor=white)
![OpenPyXL](https://img.shields.io/badge/OpenPyXL-Excel-217346?style=flat-square&logoColor=white)

---

## Funcionalidades

| Módulo                                                                                          | Estado                      |
| ----------------------------------------------------------------------------------------------- | --------------------------- |
| **OCR de etiquetas** — Foto → preprocesamiento → JSON estructurado con Claude Vision            | ✅ Listo                     |
| **Dictado de voz** — Audio → Groq Whisper → Claude → JSON de inventario                         | ✅ Listo                     |
| **Contexto de sesión** — Soporte multi-usuario con técnico asignado, pabellón/laboratorio/armario automatizado | ✅ Listo                     |
| **Dashboard de sesión** — Listado filtrado por técnico en tiempo real, con opción de deshacer | ✅ Listo                     |
| **Búsqueda rápida** — Buscar activos por nombre, modelo o número de serie con paginación | ✅ Listo                     |
| **Exportar PDF/Excel Sesión** — Reporte con columna de Técnico responsable y estadísticas | ✅ Listo                     |
| **Exportar PDF/Excel Global** — Reporte consolidado de todo el inventario con trazabilidad por técnico | ✅ Listo                     |

---

## Arquitectura del Proyecto

```
tecsup-inventory-api/
│
├── main.py                          # Entrada de la app, CORS, registro de routers
├── .env                             # Variables de entorno (no subir al repo)
├── .env.example                     # Plantilla de variables sin valores reales
├── requirements.txt
├── database.db                      # SQLite generado en runtime (gitignored)
│
├── core/
│   ├── config.py                    # Carga de variables de entorno con pydantic-settings
│   ├── database.py                  # Conexión SQLite y creación de tablas
│   └── dependencies.py              # Dependencias reutilizables de FastAPI
│
├── routes/
│   ├── ocr.py                       # POST /api/ocr/escanear-etiqueta y /confirmar
│   ├── voz.py                       # POST /api/voz/dictar y /confirmar
│   ├── sesion.py                    # GET/POST/PATCH /api/sesion/contexto
│   ├── dashboard.py                 # GET /api/dashboard/activos
│   ├── busqueda.py                  # GET /api/busqueda?q=...
│   └── exportar.py                  # GET /api/exportar/pdf y /excel
│
├── services/
│   ├── claude_service.py            # Llamadas a Claude Vision y Claude texto
│   ├── whisper_service.py           # Transcripción de audio con Groq Whisper API
│   ├── sesion_service.py            # Lógica de contexto y jornada activa
│   ├── activo_service.py            # CRUD y búsqueda en SQLite
│   ├── pdf_service.py               # Generación del PDF de resumen con ReportLab
│   └── excel_service.py             # Generación del Excel de resumen con OpenPyXL
│
├── models/
│   ├── activo.py                    # Modelo SQLite del activo
│   └── sesion.py                    # Modelo SQLite de la sesión
│
├── schemas/
│   ├── activo.py                    # Pydantic: request y response de activos
│   ├── sesion.py                    # Pydantic: request y response de sesión
│   ├── ocr.py                       # Pydantic: response del escaneo de etiqueta
│   └── voz.py                       # Pydantic: response del dictado de voz
│
├── prompts/
│   ├── ocr_prompt.py                # Prompt estructurado para Claude Vision
│   └── voz_prompt.py                # Prompt estructurado para Claude texto
│
└── utils/
    ├── image_utils.py               # Preprocesamiento de imagen (resize)
    └── audio_utils.py               # Validación de formato de audio
```

---

## Variables de Entorno

Copia el archivo de ejemplo antes de iniciar:

```bash
cp .env.example .env
```

| Variable            | Descripción                             | Ejemplo       |
| ------------------- | --------------------------------------- | ------------- |
| `ANTHROPIC_API_KEY` | API Key de Anthropic (Claude Vision)    | `sk-ant-...`  |
| `GROQ_API_KEY`      | API Key de Groq (Whisper transcripción) | `gsk_...`     |
| `APP_ENV`           | Entorno de ejecución                    | `development` |
| `APP_HOST`          | Host del servidor                       | `0.0.0.0`     |
| `APP_PORT`          | Puerto del servidor                     | `8000`        |

---

## Instalación y Setup

### Prerrequisitos

- Python 3.11+
- ffmpeg (requerido para validación de audio)

```bash
# Fedora
sudo dnf install python3 python3-pip ffmpeg -y

# Ubuntu/Debian
sudo apt install python3 python3-pip ffmpeg -y
```

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
# Edita .env y agrega tus API Keys de Anthropic y Groq
```

**5. Levantar el servidor**

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

La API estará disponible en `http://localhost:8000`.  
La documentación interactiva estará en `http://localhost:8000/docs`.

Para acceder desde el celular (misma red WiFi):

```
http://TU_IP_LOCAL:8000/docs
```

> Puedes ver tu IP local con `ip addr show` en Linux.

---

## Comandos Disponibles

| Comando                                       | Descripción                                             |
| --------------------------------------------- | ------------------------------------------------------- |
| `uvicorn main:app --reload`                   | Servidor en modo desarrollo con hot-reload              |
| `uvicorn main:app --host 0.0.0.0 --port 8000` | Servidor accesible desde la red local (para el celular) |

---

## Mantenimiento y Reset

Si deseas limpiar todos los datos y volver a cargar el seeder de prueba:

**1. Borrar la base de datos actual**
```bash
rm database.db
```

**2. Ejecutar el seeder**
```bash
python scripts/seed_db.py
```

Esto recreará las tablas y poblará el sistema con datos de prueba realistas (técnicos, dispositivos de Tecsup, etc.).

---

## Documentación API

Una vez levantado el servidor, la documentación interactiva estará disponible en:

```
http://localhost:8000/docs
```

### Endpoints principales

#### OCR de etiquetas

```
POST /api/ocr/escanear-etiqueta
```

Recibe una foto de etiqueta y devuelve los datos del dispositivo en JSON:

```json
{
  "nombre": "UPRtek MK350S Premium",
  "marca": "UPRtek",
  "modelo": "MK350S Premium",
  "tipo": "Espectrómetro/Medidor",
  "numero_serie": "HS228IAE001D",
  "observaciones": "Dispositivo made in Taiwan. Cumple con normativas RoHS, CE y FCC.",
  "confianza": "alta",
  "texto_raw": "UPRtek MK350S PREMIUM MADE IN TAIWAN RoHS CE FCC HS228IAE001D"
}
```

```
POST /api/ocr/confirmar
```

El técnico revisó el formulario y confirma el guardado. Se aplica automáticamente el contexto de sesión activa.

#### Dictado de voz

```
POST /api/voz/dictar
```

Recibe un archivo de audio (`.m4a`, `.wav`, `.mp3`, `.ogg`, `.webm`), lo transcribe con Groq Whisper y lo interpreta con Claude.

Si el técnico dicta un **activo para registrar**, la respuesta será algo como:

```json
{
  "transcripcion": "Laptop Dell Latitude 5420, serial ABC123, laboratorio 3, está en buen estado",
  "nombre": "Dell Latitude 5420",
  "marca": "Dell",
  "modelo": "Latitude 5420",
  "tipo": "Laptop",
  "numero_serie": "ABC123",
  "estado": "Bueno",
  "ubicacion": "Laboratorio 3",
  "observaciones": null,
  "es_consulta": false,
  "respuesta_consulta": null,
  "query_busqueda": null,
  "tipo_consulta": null,
  "resultados": null
}
```

Si en cambio el audio es una **consulta** (por ejemplo: "¿dónde está la laptop Dell del laboratorio 3?"), la API detecta que es una pregunta y ejecuta automáticamente la búsqueda en SQLite. En ese caso la respuesta será algo como:

```json
{
  "transcripcion": "¿dónde está la laptop Dell del laboratorio 3?",
  "nombre": null,
  "marca": null,
  "modelo": null,
  "tipo": null,
  "numero_serie": null,
  "estado": null,
  "ubicacion": null,
  "observaciones": null,
  "es_consulta": true,
  "respuesta_consulta": "¿Dónde se encuentra la laptop Dell del laboratorio 3?",
  "query_busqueda": "laptop Dell laboratorio 3",
  "tipo_consulta": "ubicacion",
  "resultados": [
    {
      "id": 42,
      "nombre": "Dell Latitude 5420",
      "marca": "Dell",
      "modelo": "Latitude 5420",
      "tipo": "Laptop",
      "numero_serie": "ABC123",
      "estado": "Bueno",
      "ubicacion": "Pabellón A / Lab 3 / Armario 1",
      "observaciones": null,
      "sesion_id": 7,
      "origen": "voz",
      "creado_en": "2025-02-10T10:15:00"
    }
  ]
}
```

```
POST /api/voz/confirmar
```

Confirma y guarda el activo dictado por voz.

#### Sesión

```
POST /api/sesion/iniciar        # Inicia jornada (requiere "tecnico", "pabellon", "laboratorio")
GET  /api/sesion/contexto       # Consulta el contexto (usa header X-Tecnico)
PATCH /api/sesion/contexto      # Actualiza ubicación (usa header X-Tecnico)
POST /api/sesion/cerrar         # Cierra sesión (usa header X-Tecnico)
```

#### Dashboard

```
GET    /api/dashboard/activos           # Lista todos los activos de la sesión activa
GET    /api/dashboard/resumen           # Resumen de la sesión: total y conteo por origen (ocr, voz, manual)
DELETE /api/dashboard/activos/{id}      # Deshace un registro (elimina de SQLite)
```

#### Búsqueda

```
GET /api/busqueda?q={término}&p=1&size=20   # Busca por nombre, modelo o número de serie con paginación
```

#### Exportación

```
GET /api/exportar/pdf           # Descarga PDF de resumen de la sesión activa
GET /api/exportar/excel         # Descarga Excel de la sesión activa
GET /api/exportar/global/pdf    # Descarga PDF de todo el inventario histórico
GET /api/exportar/global/excel  # Descarga Excel de todo el inventario histórico
```

---

## Licencia

Este proyecto está bajo la licencia **MIT**.