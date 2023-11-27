from django.urls import path
from .views import agregar_al_carrito, ver_carrito, realizar_pedido, procesar_pedido, procesar_pago

urlpatterns = [
    path('agregar-al-carrito/<int:producto_id>/', agregar_al_carrito, name='agregar_al_carrito'),
    path('carrito/', ver_carrito, name='ver_carrito'),
    path('realizar_pedido/', realizar_pedido, name='realizar_pedido'),
    path('procesar_pedido/', procesar_pedido, name='procesar_pedido'),
    path('procesar_pago/', procesar_pago, name='procesar_pago')
]