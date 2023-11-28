from django.shortcuts import render, redirect, get_object_or_404

from cesta.forms import DatosPagoForm, DatosPedidoForm
from .models import Pedido, Producto, Carrito, ItemCarrito, DatosPedido
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from django.urls import reverse

import json

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

        if form.is_valid():
            
            datos_pedido = form.save(commit=False)
            carrito = Carrito.objects.get(usuario=request.user)

            # Intenta obtener un DatosPedido existente asociado al Carrito
            try:
                datos_pedido_existente = DatosPedido.objects.get(carrito=carrito)
            except DatosPedido.DoesNotExist:
                datos_pedido_existente = None

            # Actualiza o crea un nuevo DatosPedido según sea necesario
            if datos_pedido_existente:
                # Si existe, actualiza los campos
                datos_pedido_existente.email = form.cleaned_data['email']
                datos_pedido_existente.first_name = form.cleaned_data['first_name']
                datos_pedido_existente.last_name = form.cleaned_data['last_name']
                datos_pedido_existente.direccion_envio = form.cleaned_data['direccion_envio']
                datos_pedido_existente.direccion_facturacion = form.cleaned_data['direccion_facturacion']
                datos_pedido_existente.instrucciones_entrega = form.cleaned_data['instrucciones_entrega']
                datos_pedido_existente.forma_entrega = form.cleaned_data['forma_entrega']
                datos_pedido_existente.telefono = form.cleaned_data['telefono']
                # Otros campos que desees actualizar
                datos_pedido_existente.save()
            else:
                # Si no existe, crea uno nuevo
                datos_pedido.carrito = carrito
                datos_pedido.save()
            return redirect('procesar_pago')  # Reemplaza con la URL adecuada
    else:
        form = DatosPedidoForm(request.POST, request=request)

    # GET
    
    carrito, created = Carrito.objects.get_or_create(usuario=request.user)
    items = carrito.items.all()
    
    return render(request, 'procesar_pedido.html', {'form': form, 'items': items, 'carrito': carrito})

    def get_form_kwargs(self):
            kwargs = super().get_form_kwargs()
            kwargs['request'] = self.request
            return kwargs

@login_required
def procesar_pago(request):
    if request.method == 'POST':
        form = DatosPagoForm(request.POST)
        print("====PREVALID")
        if form.is_valid():
            print("====VALID")
            
            datos_pago = form.save(commit=False)
            # form.cleaned_data['forma_pago']
            carrito = Carrito.objects.get(usuario=request.user)
            datos_pedido = DatosPedido.objects.get(carrito=carrito)
            
            productos = []
            
            for item in carrito.items.all():
                producto_info = {
                    'id': item.producto.id,
                    'nombre': item.producto.nombre,
                    'precio': float(item.producto.precio),  # Convertir Decimal a float
                    'cantidad': item.cantidad,
                    'subtotal': float(item.calcular_subtotal()),  # Convertir Decimal a float
                }
                productos.append(producto_info)
            
            
            
            
            pedido = Pedido(
                usuario=request.user,
                telefono=datos_pedido.telefono,
                direccion_envio=datos_pedido.direccion_envio,
                direccion_facturacion=datos_pedido.direccion_facturacion,
                instrucciones_entrega=datos_pedido.instrucciones_entrega,
                email=datos_pedido.email,
                first_name=datos_pedido.first_name,
                last_name=datos_pedido.last_name,
                forma_entrega=datos_pedido.forma_entrega,
                forma_pago=datos_pedido.forma_pago,
                productos=json.dumps(productos),
                precio=carrito.calcular_total()
            )

            pedido.save()

            factura_url = reverse('generar_factura', kwargs={'pedido_id': pedido.id})
            return redirect(factura_url)
    else:
        form = DatosPagoForm(request.POST)

    # GET
    
    carrito, created = Carrito.objects.get_or_create(usuario=request.user)
    items = carrito.items.all()
    
    return render(request, 'procesar_pago.html', {'form': form, 'items': items})

    def get_form_kwargs(self):
            kwargs = super().get_form_kwargs()
            kwargs['request'] = self.request
            return kwargs
        
        

