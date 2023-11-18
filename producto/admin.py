from django.contrib import admin
from .models import Producto

class ProductoAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'marca', 'modelo', 'descripcion', 'precio', 'imagen', 'unidades', 'capacidad_viajar', 'capacidad_dormir']  # Campos a mostrar en la lista de productos
    search_fields = ['nombre', 'marca', 'modelo']  # Habilita la búsqueda por nombre, marca y modelo

admin.site.register(Producto, ProductoAdmin)
