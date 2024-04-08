import unittest
from app import cargar_usuarios, guardar_usuarios, cargar_equipos, guardar_equipos

class TestUsuarios(unittest.TestCase):
    def test_cargar_usuarios(self):
        usuarios = cargar_usuarios()
        self.assertIsInstance(usuarios, dict)
        self.assertIn("usuarios", usuarios)
        self.assertIsInstance(usuarios["usuarios"], list)

    def test_guardar_usuarios(self):
        usuario = {"nombre": "Test User", "email": "test@example.com", "password": "test123"}
        guardar_usuarios({"usuarios": [usuario]})
        usuarios = cargar_usuarios()
        self.assertIn(usuario, usuarios["usuarios"])

class TestEquipos(unittest.TestCase):
    def test_cargar_equipos(self):
        equipos = cargar_equipos()
        self.assertIsInstance(equipos, dict)
        self.assertIn("equipos", equipos)
        self.assertIsInstance(equipos["equipos"], list)

    def test_guardar_equipos(self):
        equipo = {"nombre": "Test Team", "logo": "logo.png", "jugadores": []}
        guardar_equipos({"equipos": [equipo]})
        equipos = cargar_equipos()["equipos"]
        self.assertIn(equipo, equipos)

if __name__ == '__main__':
    unittest.main()
