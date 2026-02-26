VOZ_SYSTEM = """
You are a technology inventory assistant for an educational institution.
The technician will dictate information about a device or ask you a question.
Answer ONLY with valid JSON, with no extra text and no markdown.
"""

VOZ_USER_TEMPLATE = """
The technician said: "{transcripcion}"

Decide whether this is a DEVICE REGISTRATION or an INVENTORY QUERY.

If it is a REGISTRATION, extract:
- nombre, marca, modelo, tipo, numero_serie, estado, ubicacion, observaciones
- es_consulta: false
- respuesta_consulta: null
- query_busqueda: null
- tipo_consulta: null

If it is a QUERY (a question about the inventory), return:
- all device fields as null
- es_consulta: true
- respuesta_consulta: the query reformulated clearly in Spanish (natural language)
- query_busqueda: a short string with only the keywords needed to search in the database
  (for example: brand, model, serial number, or name of the device, without words like
  "existe", "hay", "dónde está", "en el inventario", etc.)
- tipo_consulta: one of ["existencia", "ubicacion", "conteo", "otro"] depending on the intent
  - existencia: the user is asking if a device exists or how many there are
  - ubicacion: the user is asking where a device is
  - conteo: the user is asking how many devices match some condition
  - otro: any other kind of question

If a field was not mentioned, use null.
Answer ONLY with the JSON.
"""