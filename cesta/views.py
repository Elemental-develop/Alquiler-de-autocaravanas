from django.shortcuts import render, redirect, get_object_or_404
from .models import Producto, Carrito, ItemCarrito
from django.http import JsonResponse

def agregar_al_carrito(request, producto_id):
    producto = get_object_or_404(Producto, pk=producto_id)
    carrito, created = Carrito.objects.get_or_create(usuario=request.user)
    item, item_created = ItemCarrito.objects.get_or_create(producto=producto, carrito=carrito)

    if not item_created:
        item.cantidad += 1
        item.save()

    return redirect('ver_carrito')

def ver_carrito(request):
    carrito, created = Carrito.objects.get_or_create(usuario=request.user)
    items = carrito.items.all()

    return render(request, 'carrito.html', {'carrito': carrito, 'items': items})