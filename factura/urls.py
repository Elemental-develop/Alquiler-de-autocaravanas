from django.urls import path
from .views import generar_factura, detalle_factura, generar_factura_pdf

urlpatterns = [
    path('generar_factura/', generar_factura, name='generar_factura'),
    path('detalle_factura/<int:factura_id>/', detalle_factura, name='detalle_factura'),
    path('detalle_factura/<int:factura_id>/generar_pdf/', generar_factura_pdf, name='generar_factura_pdf'),
]
