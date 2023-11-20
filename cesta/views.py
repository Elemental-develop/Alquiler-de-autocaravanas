from django.shortcuts import render, redirect, get_object_or_404

from cesta.forms import DatosPedidoForm
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


@login_required
def realizar_pedido(request):
    if request.method == "POST":
        user = request.user
        carrito, created = Carrito.objects.get_or_create(usuario=user)

        # Almacenamos en diccionario datos del formulario para
        # manejarlos de manera comoda
        dicc = {}

        for clave, valor in request.POST.items():
            if clave.startswith("producto_id_"):
                id = int(clave.split("producto_id_")[1])
                dicc[id] = [valor]
        
        for clave, valor in request.POST.items():
            if clave.startswith("cantidad_"):
                id = int(clave.split("cantidad_")[1])
                dicc[id].append(valor)

        # Sincronizamos cantidades en la DB
        for producto_id, cantidad in dicc.values():
            producto = Producto.objects.get(pk=producto_id)
            item, created = ItemCarrito.objects.get_or_create(carrito=carrito, producto=producto)
            item.cantidad = cantidad
            item.save()
        
        # Cambiar a una template de la siguiente fase
        # de la compra
        return redirect('procesar_pedido')

@login_required
def procesar_pedido(request):
    if request.method == 'POST':
        form = DatosPedidoForm(request.POST, request=request)
        print("=== ANTES VALIDACION")
        print(form.errors)
        if form.is_valid():
            print("=== VALIDADO")
            
            datos_pedido = form.save(commit=False)
            carrito = Carrito.objects.get(usuario=request.user)
            # Asigna el carrito actual
            print("====DATOS PEDIDO")
            print(carrito)
            datos_pedido.carrito = carrito
            
            print(datos_pedido)
            datos_pedido.save()
            return HttpResponse('PÁGINA DE PAGO')  # Reemplaza con la URL adecuada
    else:
        form = DatosPedidoForm(request.POST, request=request)

    # GET
    
    carrito, created = Carrito.objects.get_or_create(usuario=request.user)
    items = carrito.items.all()
    
    return render(request, 'procesar_pedido.html', {'form': form, 'items': items})

    def get_form_kwargs(self):
            kwargs = super().get_form_kwargs()
            kwargs['request'] = self.request
            return kwargs