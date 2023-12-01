from django.test import Client, TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from producto.models import Producto

# Create your tests here.
class CompraTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.user.save()
        self.producto = Producto.objects.create(id=1, nombre='Producto 1', precio=1000, categoria='Categoria 1')  
        self.producto.save()


    
    def test_cesta(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get('/cesta/carrito/')
        
        self.assertEqual(response.status_code, 200)
        
    def test_cesta_wrong(self):
        
        response = self.client.get('/cesta/carrito/')
        self.assertEqual(response.status_code, 302)
    