## Tecsup Inventory API – Guía de pruebas en `/docs`

Esta guía explica, paso a paso, cómo probar **todas las funcionalidades** de la API usando la documentación interactiva de FastAPI en `http://localhost:8000/docs`.

Antes de empezar:

- Tener el servidor levantado:

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

- Tener configuradas las variables de entorno en `.env`:
  - `ANTHROPIC_API_KEY`
  - `GROQ_API_KEY`

---

## 1. Flujo de sesión (contexto de jornada)

La sesión define el **pabellón / laboratorio / armario** que se aplicará automáticamente a los activos registrados.

### 1.1 Iniciar sesión de jornada

- Endpoint: `POST /api/sesion/iniciar`
- En `/docs`, haz clic en el endpoint, luego en **Try it out**.
- Body de ejemplo:

```json
{
  "pabellon": "Pabellón A",
  "laboratorio": "Lab 3",
  "armario": "Armario 1"
}
```

- Pulsa **Execute**.
- Respuesta esperada:
  - Código `200`.
  - JSON con `id`, `pabellon`, `laboratorio`, `armario`, `activa: 1`.

### 1.2 Consultar contexto actual

- Endpoint: `GET /api/sesion/contexto`
- Simplemente pulsa **Execute**.
- Debe devolver la misma información de la sesión activa.
- Si no hay sesión activa, devolverá `404`.

### 1.3 Actualizar contexto sin cerrar sesión

- Endpoint: `PATCH /api/sesion/contexto`
- Body de ejemplo (solo cambiando laboratorio):

```json
{
  "laboratorio": "Lab 4"
}
```

- Respuesta:
  - La sesión sigue siendo la misma (`id`), pero con `laboratorio` actualizado.

### 1.4 Cerrar sesión

- Endpoint: `POST /api/sesion/cerrar`
- Respuesta:

```json
{
  "mensaje": "Sesión cerrada correctamente."
}
```

- A partir de aquí, endpoints que dependen de sesión activa (`dashboard`, `exportar`, etc.) devolverán `404` hasta iniciar una nueva sesión.

---

## 2. Flujo de OCR (foto de etiqueta)

### 2.1 Escanear etiqueta con OCR

- Endpoint: `POST /api/ocr/escanear-etiqueta`
- En `/docs`:
  - Haz clic en el endpoint.
  - **Try it out**.
  - En el campo `imagen`, selecciona un archivo de imagen (`.jpg`, `.jpeg`, `.png`, `.webp`, `.heic`).
  - Idealmente, la foto debe mostrar **la etiqueta y, si se puede, el dispositivo completo**. Claude Vision usará tanto el texto de la etiqueta como la apariencia del dispositivo para inferir `tipo`, `modelo`, etc.
- Pulsa **Execute**.
- Respuesta esperada (`200`):

```json
{
  "nombre": "Monitor Dell P2422H",
  "marca": "Dell",
  "modelo": "P2422H",
  "tipo": "Monitor",
  "numero_serie": "5KRG2P3",
  "observaciones": null,
  "confianza": "alta",
  "texto_raw": "DELL P2422H S/N: 5KRG2P3 Made in China"
}
```

### 2.2 Confirmar y guardar el activo leído por OCR

- Asegúrate de tener una **sesión activa** (sección 1).
- Endpoint: `POST /api/ocr/confirmar`
- En `/docs`:
  - Copia el JSON de respuesta del paso 2.1.
  - Ajusta los campos que quieras corregir/rellenar (por ejemplo `observaciones`).
  - En el body, envía algo como:

```json
{
  "nombre": "Monitor Dell P2422H",
  "marca": "Dell",
  "modelo": "P2422H",
  "tipo": "Monitor",
  "numero_serie": "5KRG2P3",
  "estado": "Bueno",
  "ubicacion": null,
  "observaciones": "Pantalla con ligero rayón en esquina",
  "sesion_id": null,
  "origen": "ocr"
}
```

- El backend:
  - Rellenará `ubicacion` automáticamente usando el contexto de sesión si está vacío.
  - Asignará `sesion_id` de la sesión activa.
  - Guardará `origen = "ocr"`.

- Respuesta esperada:
  - Código `200`.
  - JSON con el activo guardado, incluyendo `id`, `sesion_id`, `origen`, `creado_en`.

---

## 3. Flujo de dictado de voz

### 3.1 Registrar un activo por voz

- Endpoint: `POST /api/voz/dictar`
- En `/docs`:
  - **Try it out**.
  - En el campo `audio`, sube un archivo `.m4a`, `.wav`, `.mp3`, `.ogg` o `.webm`.
  - Ejemplo de frase (en español):  
    `"Laptop Dell Latitude 5420, serial ABC123, laboratorio 3, está en buen estado"`
- Pulsa **Execute**.
- Respuesta esperada (caso REGISTRO):

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
  "resultados": null
}
```

### 3.2 Confirmar y guardar el activo dictado por voz

- Endpoint: `POST /api/voz/confirmar`
- Body de ejemplo (basado en la respuesta anterior):

```json
{
  "nombre": "Dell Latitude 5420",
  "marca": "Dell",
  "modelo": "Latitude 5420",
  "tipo": "Laptop",
  "numero_serie": "ABC123",
  "estado": "Bueno",
  "ubicacion": null,
  "observaciones": null,
  "sesion_id": null,
  "origen": "voz"
}
```

- Igual que en OCR:
  - El backend aplicará la ubicación de sesión si `ubicacion` está vacío.
  - Asignará `sesion_id` y `origen = "voz"`.

### 3.3 Hacer una consulta por voz (búsqueda automática)

- Endpoint: `POST /api/voz/dictar`
- Ejemplo de audio:  
  `"¿Dónde está la laptop Dell del laboratorio 3?"`
- Respuesta esperada (caso CONSULTA):

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

- El frontend puede:
  - Mostrar `respuesta_consulta` como texto de la búsqueda.
  - Listar `resultados` como tarjetas/tabla de activos.

---

## 4. Dashboard de sesión

### 4.1 Listar activos de la sesión activa

- Endpoint: `GET /api/dashboard/activos`
- Requiere sesión activa.
- Respuesta: lista de activos (`ActivoResponse`) asociados a la sesión actual.

### 4.2 Ver resumen de la sesión

- Endpoint: `GET /api/dashboard/resumen`
- Respuesta de ejemplo:

```json
{
  "total": 15,
  "por_origen": {
    "ocr": 8,
    "voz": 5,
    "manual": 2
  }
}
```

- Útil para mostrar estadísticas en el frontend (por ejemplo, donuts o contadores).

### 4.3 Deshacer un registro

- Endpoint: `DELETE /api/dashboard/activos/{id}`
- En `/docs`:
  - Introduce un `id` existente de un activo.
- Respuesta:

```json
{
  "mensaje": "Activo 42 eliminado."
}
```

---

## 5. Búsqueda rápida

### 5.1 Buscar por nombre, modelo o número de serie

- Endpoint: `GET /api/busqueda`
- En `/docs`:
  - Parámetro `q` (obligatorio, mínimo 1 carácter).
  - Ejemplos:
    - `q = "Latitude"`
    - `q = "ABC123"`
    - `q = "Monitor"`
- Respuesta:
  - Lista de activos que coinciden parcialment por `nombre`, `modelo` o `numero_serie`.

---

## 6. Exportación de reportes

Requieren sesión activa y al menos un activo registrado.

### 6.1 Exportar PDF de resumen

- Endpoint: `GET /api/exportar/pdf`
- En `/docs`, pulsa **Execute**.
- La respuesta será un archivo PDF descargable con:
  - Resumen de la sesión.
  - Tabla de activos.
  - Estadísticas por origen.

### 6.2 Exportar Excel de resumen

- Endpoint: `GET /api/exportar/excel`
- La respuesta será un archivo `.xlsx` con:
  - Hoja 1: resumen de jornada.
  - Hoja 2: tabla completa de activos con autofiltro.

---

## 7. Comprobaciones rápidas de salud

### 7.1 Endpoint raíz

- Endpoint: `GET /`
- Respuesta de ejemplo:

```json
{
  "estado": "ok",
  "ambiente": "development"
}
```

Si llega esta respuesta, el servidor y la configuración básica están funcionando.

