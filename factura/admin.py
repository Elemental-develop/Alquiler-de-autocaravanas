from django.contrib import admin
from .models import Factura

class FacturaAdmin(admin.ModelAdmin):
    list_display = ['id', 'cliente', 'fecha_emision', 'total']  # Campos a mostrar en la lista de facturas
    search_fields = ['cliente']  # Habilita la búsqueda por cliente
    filter_horizontal = ['productos']  # Agrega una interfaz de selección de productos

admin.site.register(Factura, FacturaAdmin)
