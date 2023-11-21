from django.contrib import admin
from .models import DatosEntrega

class DatosEntregaAdmin(admin.ModelAdmin):
    list_display = ('user', 'direccion_entrega', 'ciudad', 'codigo_postal', 'metodo_pago')

admin.site.register(DatosEntrega, DatosEntregaAdmin)
