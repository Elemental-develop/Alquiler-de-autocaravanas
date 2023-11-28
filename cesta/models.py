from enum import Enum, auto
from django.db import models
from producto.models import Producto
from django.contrib.auth.models import User
from django.utils import timezone

class Carrito(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    productos = models.ManyToManyField(Producto, through='ItemCarrito')

    def calcular_total(self):
        return sum(item.calcular_subtotal() for item in self.items.all())
    
    def limpiar_carrito(self):
        self.productos.clear()

class ItemCarrito(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    carrito = models.ForeignKey(Carrito, on_delete=models.CASCADE, related_name='items')
    cantidad = models.PositiveIntegerField(default=1)

    def calcular_subtotal(self):
        return self.producto.precio * self.cantidad


class FormaEntrega(models.TextChoices):
    ESTANDAR = 'EST', 'Estándar'
    URGENTE = 'URG', 'Urgente'
    VEINTICUATRO_HORAS = '24H', '24 horas'


class FormaPago(models.TextChoices):
    CONTRARREEMBOLSO = 'CONT', 'Contrareembolso'
    STRIPE = 'STRIPE', 'Pago con Stripe'
    
    
class DatosPedido(models.Model):
    carrito = models.OneToOneField(Carrito, on_delete=models.CASCADE)

    forma_entrega = models.CharField(
        max_length=5,
        choices=FormaEntrega.choices,
        default=FormaEntrega.ESTANDAR,
    )
    
    forma_pago = models.CharField(
        max_length=10,
        choices=FormaPago.choices,
        default=FormaPago.CONTRARREEMBOLSO
    )
    
    telefono = models.CharField(max_length=12)
    direccion_envio = models.CharField(max_length=150)
    direccion_facturacion = models.CharField(max_length=150)
    instrucciones_entrega = models.TextField()

    # Agrega campos del User asociado al Carrito
    email = models.EmailField(default="")
    first_name = models.CharField(max_length=30, default="")
    last_name = models.CharField(max_length=30, default="")

    def __str__(self):
        return f'Datos de Pedido para el Carrito {self.carrito.id}'


class Estado(models.TextChoices):
    ENTREGADO = 'ENTREGADO', 'Entregado'
    CONFIRMADO = 'CONFIRMADO', 'Confirmado'
    PENDIENTE = 'PENDIENTE', 'Pendiente'

class Pedido(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)

    telefono = models.CharField(max_length=12)
    direccion_envio = models.CharField(max_length=150)
    direccion_facturacion = models.CharField(max_length=150)
    instrucciones_entrega = models.TextField()
    
    email = models.EmailField(default="")
    first_name = models.CharField(max_length=30, default="")
    last_name = models.CharField(max_length=30, default="")
    
    forma_entrega = models.CharField(
        max_length=5,
        choices=FormaEntrega.choices,
        default=FormaEntrega.ESTANDAR,
    )
    
    forma_pago = models.CharField(
        max_length=10,
        choices=FormaPago.choices,
        default=FormaPago.CONTRARREEMBOLSO
    )
    
    # Nuevo campo para productos (en formato JSON)
    productos = models.TextField(default="")

    # Nueva fecha de creación
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    # Nuevo campo para el estado
    estado = models.CharField(
        max_length=15,
        choices=Estado.choices,
        default=Estado.PENDIENTE
    )
    
    precio = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
