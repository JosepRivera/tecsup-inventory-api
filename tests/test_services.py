import pytest
import sqlite3
from services.sesion_service import normalizar_texto, crear_sesion, obtener_sesion_activa, cerrar_sesion
from services.activo_service import guardar_activo, listar_activos_sesion, obtener_activo, buscar_activos

def test_normalizar_texto():
    assert normalizar_texto("  laboratorio3  ") == "Laboratorio 3"
    assert normalizar_texto("pab A") == "Pabellón A"
    assert normalizar_texto("hola mundo") == "Hola Mundo"
    assert normalizar_texto("") == ""

def test_sesion_crud(db_conn):
    # Crear sesión
    sesion = crear_sesion(db_conn, "Josep Rivera", "Pabellon A", "Lab 1", "Armario 1")
    assert sesion["tecnico"] == "Josep Rivera"
    assert sesion["activa"] == 1
    
    # Obtener activa
    activa = obtener_sesion_activa(db_conn, "Josep Rivera")
    assert activa["id"] == sesion["id"]
    
    # Cerrar sesión
    cerrar_sesion(db_conn, sesion["id"])
    activa_despues = obtener_sesion_activa(db_conn, "Josep Rivera")
    assert activa_despues is None

def test_activo_crud(db_conn):
    # Crear sesión primero
    sesion = crear_sesion(db_conn, "Test Tech", "Pab B", "Lab 2", "Arm 2")
    
    # Guardar activo
    datos = {
        "sesion_id": sesion["id"],
        "nombre": "Monitor LG",
        "marca": "LG",
        "modelo": "24MK430H",
        "tipo": "Monitor",
        "numero_serie": "SN12345",
        "estado": "Bueno",
        "ubicacion": "Lab 2",
        "origen": "manual"
    }
    activo = guardar_activo(db_conn, datos)
    assert activo["nombre"] == "Monitor LG"
    assert activo["sesion_id"] == sesion["id"]
    
    # Listar por sesión
    lista = listar_activos_sesion(db_conn, sesion["id"])
    assert len(lista) == 1
    assert lista[0]["nombre"] == "Monitor LG"
    
    # Buscar
    resultados = buscar_activos(db_conn, "Monitor")
    assert len(resultados) == 1
    assert resultados[0]["nombre"] == "Monitor LG"
    
    # Obtener por ID
    recuperado = obtener_activo(db_conn, activo["id"])
    assert recuperado["id"] == activo["id"]
