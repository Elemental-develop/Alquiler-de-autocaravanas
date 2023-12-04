from django.db import models

class Reclamacion(models.Model):
    titulo = models.CharField(max_length=255)
    descripcion = models.TextField()
    fecha = models.DateField(auto_now_add=True)
