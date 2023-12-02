from django.urls import path
from .views import agregar_al_carrito, cancelar_pago_stripe, exito_pago_stripe, ver_carrito, realizar_pedido, procesar_pedido, procesar_pago, eliminar_del_carrito

urlpatterns = [
    path('agregar-al-carrito/<int:producto_id>/', agregar_al_carrito, name='agregar_al_carrito'),
    path('eliminar_del_carrito/<int:producto_id>/', eliminar_del_carrito, name='eliminar_del_carrito'),
    path('carrito/', ver_carrito, name='ver_carrito'),
    path('realizar_pedido/', realizar_pedido, name='realizar_pedido'),
    path('procesar_pedido/', procesar_pedido, name='procesar_pedido'),
    path('procesar_pago/', procesar_pago, name='procesar_pago'),
    path('exito_pago_stripe/', exito_pago_stripe, name='exito_pago_stripe'),
    path('cancelar_pago_stripe/', cancelar_pago_stripe, name='cancelar_pago_stripe')
]