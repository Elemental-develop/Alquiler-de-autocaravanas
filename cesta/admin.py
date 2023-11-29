from django.contrib import admin
from .models import Pedido

class PedidoAdmin(admin.ModelAdmin):
    list_display = ['id', 'usuario', 'forma_entrega', 'forma_pago', 'estado', 'fecha_creacion']
    search_fields = ['usuario__username', 'direccion_envio', 'direccion_facturacion']

admin.site.register(Pedido, PedidoAdmin)
