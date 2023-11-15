from django.shortcuts import get_object_or_404, render, redirect
from producto.models import Producto
from django.db.models import Q


def home(request):
    # Query params
    busqueda_q = request.GET.get('q', '')
    busqueda_marca = request.GET.get('marca', '')
    busqueda_precio_min = request.GET.get('precio_min', '')
    busqueda_precio_max = request.GET.get('precio_max', '')
    
    # Obtener todas las marcas distintas de la base de datos
    marcas_distintas = Producto.objects.values('marca').distinct()
    # Convertir el resultado a una lista de marcas
    marcas = [marca['marca'] for marca in marcas_distintas]
    
    marca = ""
    
    # Construir la consulta de manera condicional
    query = Q()
    
    if busqueda_q:
        query &= Q(nombre__icontains = busqueda_q) | Q(descripcion__icontains = busqueda_q)
    
    if busqueda_marca:
        query &= Q(marca__icontains=busqueda_marca)
    
    if busqueda_precio_min:
        query &= Q(precio__gte=float(busqueda_precio_min))
    
    if busqueda_precio_max:
        query &= Q(precio__lte=float(busqueda_precio_max))

    productos = Producto.objects.filter(query).distinct()

    return render(request, "lista_productos.html", {'productos': productos, 'marcas': marcas,'busqueda_q': busqueda_q, 'busqueda_marca': busqueda_marca, 'busqueda_precio_min': busqueda_precio_min, 'busqueda_precio_max': busqueda_precio_max})
