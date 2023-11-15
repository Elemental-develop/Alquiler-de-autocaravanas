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