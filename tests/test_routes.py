import pytest
from fastapi.testclient import TestClient

def test_root(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["estado"] == "ok"

def test_sesion_endpoints(client):
    # Iniciar sesión
    payload = {
        "tecnico": "Josep",
        "pabellon": "pab A",
        "laboratorio": "Lab 101",
        "armario": "C1"
    }
    response = client.post("/api/sesion/iniciar", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["pabellon"] == "Pabellón A" # Por normalización
    
    # Obtener contexto con header
    headers = {"X-Tecnico": "Josep"}
    response = client.get("/api/sesion/contexto", headers=headers)
    assert response.status_code == 200
    assert response.json()["id"] == data["id"]

def test_activos_pagination(client):
    # Sin técnico, debería poder listar todos
    response = client.get("/api/activos/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_dashboard_resumen_error_no_sesion(client):
    # Un técnico sin sesión activa debería dar 404
    headers = {"X-Tecnico": "Tecnico Fantasma"}
    response = client.get("/api/dashboard/resumen", headers=headers)
    assert response.status_code == 404
