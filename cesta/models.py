from django.db import models
from producto.models import Producto
from django.contrib.auth.models import User

class Carrito(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    productos = models.ManyToManyField(Producto, through='ItemCarrito')

    def calcular_total(self):
        return sum(item.calcular_subtotal() for item in self.items.all())
    
class ItemCarrito(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    carrito = models.ForeignKey(Carrito, on_delete=models.CASCADE, related_name='items')
    cantidad = models.PositiveIntegerField(default=1)

    def calcular_subtotal(self):
        return self.producto.precio * self.cantidad

class DatosPedido(models.Model):
    carrito = models.ForeignKey(Carrito, on_delete=models.CASCADE)
    telefono = models.CharField(max_length=20)
    direccion_envio = models.CharField(max_length=150)
    direccion_facturacion = models.CharField(max_length=150)
    instrucciones_entrega = models.TextField()

    # Agrega campos del User asociado al Carrito
    email = models.EmailField(default="")
    first_name = models.CharField(max_length=30, default="")
    last_name = models.CharField(max_length=30, default="")

    def __str__(self):
        return f'Datos de Pedido para el Carrito {self.carrito.id}'