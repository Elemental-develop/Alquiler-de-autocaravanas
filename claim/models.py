from django.db import models

class Claim(models.Model):
    titulo = models.CharField(max_length=255)
    descripcion = models.TextField()
    fecha = models.DateField(auto_now_add=True)
