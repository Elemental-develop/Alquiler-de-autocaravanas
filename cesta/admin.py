from django.contrib import admin
from django.db.models import Sum, Avg
from .models import Pedido

class PedidoAdmin(admin.ModelAdmin):
    list_display = ['id', 'usuario', 'forma_entrega', 'forma_pago', 'estado', 'fecha_creacion', 'precio']
    search_fields = ['usuario__username', 'direccion_envio', 'direccion_facturacion']

    actions = ['calcular_total_ventas', 'calcular_media_precios']

    def calcular_total_ventas(self, request, queryset):
        total_ventas = queryset.aggregate(Sum('precio'))['precio__sum'] or 0.00
        self.message_user(request, f'Total de ventas seleccionadas: {total_ventas:.2f}€')

    calcular_total_ventas.short_description = 'Calcular total de ventas seleccionadas'

    def calcular_media_precios(self, request, queryset):
        media_precios = queryset.aggregate(Avg('precio'))['precio__avg'] or 0.00
        self.message_user(request, f'Media de precios de ventas seleccionadas: {media_precios:.2f}€')

    calcular_media_precios.short_description = 'Calcular media de precios de ventas seleccionadas'

admin.site.register(Pedido, PedidoAdmin)
