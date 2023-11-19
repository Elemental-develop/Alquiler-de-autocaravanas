from django.shortcuts import render

from producto.forms import OpinionForm
from .models import Producto
from oferta.models import Oferta

from django.shortcuts import render, get_object_or_404

def lista_productos(request):
    
    productos = Producto.objects.all()
    ofertas = Oferta.objects.all()
      
    return render(request, 'lista_productos.html', {'productos': productos})

def detalles_producto(request, producto_id):
    producto = get_object_or_404(Producto, pk=producto_id)
    lista_opiniones = []
    for opinion in producto.opiniones.split(','):
        lista_opiniones.append(opinion)
    if request.method == 'POST':
        form = OpinionForm(request.POST)
        if form.is_valid():
            nueva_opinion = form.cleaned_data['opinion']
            
            producto.agregar_opinion(nueva_opinion)
            lista_opiniones.append(nueva_opinion)
            render(request, 'detalles_producto.html', {'producto': producto, 'opinion_form': form, 'opiniones': lista_opiniones})
    else:
        form = OpinionForm()
    lista_opiniones.__delitem__(1)
    lista_opiniones.__delitem__(0)
    return render(request, 'detalles_producto.html', {'producto': producto, 'opinion_form': form, 'opiniones': lista_opiniones})
   