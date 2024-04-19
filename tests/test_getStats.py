import pytest
from flask import json
from getStats import create_app  # Asumiendo que la función create_app() configura y retorna una instancia de Flask

@pytest.fixture
def client():
    app = create_app()
    app.config.update({
        "TESTING": True,
    })

    with app.test_client() as client:
        yield client

def test_obtener_info_jugadores(client):
    response = client.post('/get_stats/obtener_info_jugadores', json={"nombre_equipo": "Equipo Test"})
    data = json.loads(response.data.decode('utf-8'))
    assert response.status_code == 200
    assert 'jugadores' in data  # Asegúrate de que 'jugadores' está en la respuesta JSON

def test_estadisticas_equipos_get(client):
    response = client.get('/get_stats/estadisticas_equipos')
    assert response.status_code == 200
    assert 'equipos_data' in response.data.decode('utf-8')  # Verifica que la plantilla recibida tiene los datos de equipos

def test_estadisticas_equipos_post(client):
    response = client.post('/get_stats/estadisticas_equipos', data={"equipo": "Equipo Test"})
    assert response.status_code == 200
    assert 'estadisticas' in response.data.decode('utf-8')  # Asegúrate de que 'estadisticas' está en la respuesta

def test_obtener_estadisticas_json(client):
    response = client.post('/get_stats/obtener_estadisticas_json', json={"nombre_equipo": "Equipo Test"})
    assert response.status_code == 200
    assert 'error' not in json.loads(response.data.decode('utf-8'))  # Verifica que no haya errores

def test_cerrar_sesion(client):
    response = client.get('/get_stats/cerrar_sesion')
    assert response.status_code == 302  # Espera un código de redirección

