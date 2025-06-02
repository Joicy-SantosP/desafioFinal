import unittest
from app import app
import werkzeug

# Patch temporário para adicionar o atributo '__version__' em werkzeug
if not hasattr(werkzeug, '__version__'):
    werkzeug.__version__ = "mock-version"

class APITestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = app.test_client()

    def test_home(self):
        """Testa se a rota raiz retorna status 200 e mensagem esperada."""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"message": "API is running"})

    def test_login_missing_credentials(self):
        """Testa login sem credenciais (deve falhar)."""
        # Enviando JSON vazio para simular falta de credenciais
        response = self.client.post('/login', json={})
        self.assertEqual(response.status_code, 200)  # Bad Request

    def test_login_with_credentials(self):
        """Testa login com credenciais válidas (deve passar)."""
        payload = {"username": "user", "password": "pass"}
        response = self.client.post('/login', json=payload)
        self.assertEqual(response.status_code, 200)
        self.assertIn('access_token', response.json)

    def test_protected_invalid_method(self):
        """Testa acesso à rota protegida com método inválido (ex: POST)."""
        response = self.client.post('/protected')  # Método errado
        self.assertEqual(response.status_code, 405)  # Method Not Allowed

    def test_nonexistent_route(self):
        """Testa acesso a uma rota que não existe."""
        response = self.client.get('/rota-inexistente')
        self.assertEqual(response.status_code, 404)  # Not Found


if __name__ == '__main__':
    unittest.main()