import unittest
from app import app
import werkzeug

# Patch temporário para adicionar o atributo '__version__' em werkzeug
if not hasattr(werkzeug, '__version__'):
    werkzeug.__version__ = "mock-version"

class APITestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Criação do cliente de teste
        cls.client = app.test_client()

    def test_home(self):
        """Testa se a rota raiz retorna status 200 e mensagem esperada."""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"message": "API is running"})

    def test_login_missing_credentials(self):
        """Testa login sem credenciais (deve falhar)."""
        response = self.client.post('/login', data={})  # Dados vazios
        self.assertEqual(response.status_code, 400)  # Bad Request

    def test_protected_invalid_method(self):
        """Testa acesso à rota protegida com método inválido (ex: POST)."""
        response = self.client.post('/protected')  # Método errado
        self.assertEqual(response.status_code, 405)  # Method Not Allowed

    def test_nonexistent_route(self):
        """Testa acesso a uma rota que não existe."""
        response = self.client.get('/rota-inexistente')
        self.assertEqual(response.status_code, 404)  # Not Found

    def test_server_header(self):
        """Verifica se o cabeçalho 'Server' está presente nas respostas."""
        response = self.client.get('/')
        self.assertIn('Server', response.headers)

if __name__ == '__main__':
    unittest.main()