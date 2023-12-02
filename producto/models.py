from django.db import models

from oferta.models import Oferta

class Producto(models.Model):

    CATEGORIAS_CHOICES = [
        ('integral', 'Autocaravana Integral'),
        ('capuchina', 'Autocaravana Capuchina'),
        ('perfilada', 'Autocaravana Perfilada'),
        ('camper', 'Autocaravana Camper'),
    ]

    nombre = models.CharField(max_length=100)
    marca = models.CharField(max_length=100)
    modelo = models.CharField(max_length=100)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    imagen = models.URLField()
    unidades = models.IntegerField(default=0)
    capacidad_viajar = models.IntegerField(default=0)
    capacidad_dormir = models.IntegerField(default=0)
    oferta = models.ForeignKey(Oferta, on_delete=models.CASCADE, null=True, default=None)
    opiniones = models.CharField(max_length=1000, blank=True, default=',')
    categoria = models.CharField(max_length=20, choices=CATEGORIAS_CHOICES, default='integral')


    def agregar_opinion(self, nueva_opinion):
        # Método para agregar una nueva opinión a la autocaravana
        if self.opiniones:
            self.opiniones += f",{nueva_opinion}"
        else:
            self.opiniones = nueva_opinion
        self.save()
        
    def precio_rebajado(self):
        if self.oferta == None:
            return self.precio
        return float(self.precio) - float(self.oferta.porcentaje)/100. * float(self.precio)

    def str(self):
        return self.nombre