from django.shortcuts import render
from .models import Producto
from oferta.models import Oferta

from django.shortcuts import render, get_object_or_404

def lista_productos(request):
        
    categoria = request.GET.get('categoria', '')
    productos = Producto.objects.all()
    
    if categoria != '':
        productos = Producto.objects.filter(categoria=categoria)

    return render(request, 'lista_productos.html', {'productos': productos})

def detalles_producto(request, producto_id):
    productos = Producto.objects.all()
    producto_seleccionado = get_object_or_404(Producto, pk=producto_id)
    return render(request, 'detalles_producto.html', {'productos': productos, 'producto_seleccionado': producto_seleccionado})