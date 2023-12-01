from django import forms
from django.contrib import admin
from .models import Factura, Factura_productos_personalizado
from producto.models import Producto

class FacturaProductosPersonalizadoInline(admin.TabularInline):
    model = Factura_productos_personalizado
    extra = 1

class FacturaAdmin(admin.ModelAdmin):
    inlines = [FacturaProductosPersonalizadoInline]

admin.site.register(Factura, FacturaAdmin)
