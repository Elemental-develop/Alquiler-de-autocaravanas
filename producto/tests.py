from django.test import TestCase, Client
from django.urls import reverse

from producto.models import Producto

class ProductoModelTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.producto = Producto.objects.create(pk=1, nombre='Producto 1', precio=1000, categoria='Categoria 1')  
        self.producto.save()

    
    def test_precio_producto(self):
        
        producto = Producto.objects.get(nombre='Producto 1')
        self.assertEqual(producto.precio, 1000)
        
    def test_detalles_producto_view(self):
        response = self.client.get(reverse('detalles_producto', args=[self.producto.id])) # type: ignore

        self.assertEqual(response.status_code, 200)
        
    def test_catalogo_view(self):
        response = self.client.get(reverse('lista_productos'))
        
        self.assertEqual(response.status_code, 200)
        
    

