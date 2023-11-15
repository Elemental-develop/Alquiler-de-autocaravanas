from django.shortcuts import get_object_or_404, render, redirect
from producto.models import Producto
from django.db.models import Q


def home(request):
    busqueda = request.GET.get('buscar')
    if busqueda:
        productos = Producto.objects.filter(
            Q(nombre__icontains = busqueda) |
            Q(modelo__icontains = busqueda)
        ).distinct
        return render(request, "lista_productos.html", {'productos': productos})
    return render(request, "home.html")
    


