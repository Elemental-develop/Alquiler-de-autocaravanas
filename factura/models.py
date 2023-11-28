from django.db import models
from cesta.models import Pedido
from producto.models import Producto

class Factura(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    fecha_emision = models.DateField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Factura {self.id} - Pedido {self.pedido.id}"

class Factura_productos_personalizado(models.Model):
    factura = models.ForeignKey(Factura, on_delete=models.CASCADE)
    producto = models.ForeignKey('producto.Producto', on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=0)

    class Meta:
        db_table = 'factura_productos_personalizado'
