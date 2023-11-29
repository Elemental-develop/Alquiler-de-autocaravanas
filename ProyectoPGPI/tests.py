
from django.contrib.auth.models import User
from django.test import Client, TestCase


class ProductoModelTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        
    def test_login(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get('/cuenta/')
        self.assertEqual(response.status_code, 200)
    
    def test_login_wrong(self):
        response = self.client.get('/cuenta/')
        self.assertEqual(response.status_code, 302)
        
           
    def test_logout_wrong(self):
        response = self.client.get('/logout/')
        self.assertEqual(response.status_code, 302)
        
class HomeViewTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_home_page(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Alquiler de Autocaravanas")
        self.assertContains(response, "Explora nuestro amplio catálogo de autocaravanas")
        # Agrega más aserciones según sea necesario