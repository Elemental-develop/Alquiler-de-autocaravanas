from django.shortcuts import render, redirect, get_object_or_404
from .models import Producto, Carrito, ItemCarrito
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required



@login_required
def agregar_al_carrito(request, producto_id):
    producto = get_object_or_404(Producto, pk=producto_id)
    carrito, created = Carrito.objects.get_or_create(usuario=request.user)
    item, item_created = ItemCarrito.objects.get_or_create(producto=producto, carrito=carrito)

    if not item_created:
        item.cantidad += 1
        item.save()

    return redirect('ver_carrito')

@login_required
def ver_carrito(request):
    carrito, created = Carrito.objects.get_or_create(usuario=request.user)
    items = carrito.items.all()

    return render(request, 'carrito.html', {'carrito': carrito, 'items': items})


def realizar_pedido(request):
    if request.method == "POST":
        # Procesar los datos del formulario
        user = request.user
        carrito, created = Carrito.objects.get_or_create(usuario=user)
        items = []

        for key, value in request.POST.items():
            if key.startswith("cantidad_"):
                producto_id = key.replace("cantidad_", "")
                cantidad = int(value)
                producto = Producto.objects.get(pk=producto_id)
                item, created = ItemCarrito.objects.get_or_create(carrito=carrito, producto=producto)
                item.cantidad = cantidad
                item.save()
                items.append(item)

        # Actualizar el carrito con los nuevos elementos
        carrito.items.set(items)
        carrito.save()

        return HttpResponse("Pedido realizado con éxito!")
    else:

        return HttpResponse("Error al realizar el pedido!")