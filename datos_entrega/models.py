from django.db import models
from django.contrib.auth.models import User

class DatosEntrega(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    direccion_entrega = models.CharField(max_length=255, blank=True, null=True)
    ciudad = models.CharField(max_length=100, blank=True, null=True)
    codigo_postal = models.CharField(max_length=20, blank=True, null=True)
    metodo_pago = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.user.username
