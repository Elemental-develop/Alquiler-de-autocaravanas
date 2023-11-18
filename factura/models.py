from django.db import models
from django.contrib.auth.models import User

class Factura(models.Model):
    cliente = models.ForeignKey(User, on_delete=models.CASCADE)
    fecha_emision = models.DateField(auto_now_add=True)
    productos = models.ManyToManyField('producto.Producto')
    total = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Factura {self.id} - {self.cliente.username}"
