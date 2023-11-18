from django.shortcuts import render
from .models import Producto
from oferta.models import Oferta

from django.shortcuts import render, get_object_or_404

def lista_productos(request):
    
    productos = Producto.objects.all()
    ofertas = Oferta.objects.all()
      
    return render(request, 'lista_productos.html', {'productos': productos})

def detalles_producto(request, producto_id):
    producto = get_object_or_404(Producto, pk=producto_id)
    return render(request, 'detalles_producto.html', {'producto': producto})