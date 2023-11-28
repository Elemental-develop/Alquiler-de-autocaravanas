from pyexpat.errors import messages
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
import stripe

from cesta.forms import DatosPagoForm, DatosPedidoForm
from cesta.utils import create_pedido, get_productos_from_carrito
from .models import Estado, FormaPago, Pedido, Producto, Carrito, ItemCarrito, DatosPedido
from django.http import HttpResponse, HttpResponseForbidden, JsonResponse
from django.contrib.auth.decorators import login_required

import json

@login_required
def agregar_al_carrito(request, producto_id):
    producto = get_object_or_404(Producto, pk=producto_id)
    carrito, created = Carrito.objects.get_or_create(usuario=request.user)
    item, item_created = ItemCarrito.objects.get_or_create(producto=producto, carrito=carrito)
    
    cantidad_param = request.GET.get('cantidad')
    
    if item_created:
        item.cantidad = cantidad_param
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
    
    return render(request, 'procesar_pedido.html', {'form': form, 'items': items})

    def get_form_kwargs(self):
            kwargs = super().get_form_kwargs()
            kwargs['request'] = self.request
            return kwargs

@login_required
def procesar_pago(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    
    if request.method == 'POST':
        form = DatosPagoForm(request.POST)
        if form.is_valid():
            datos_pedido = DatosPedido.objects.get(carrito__usuario=request.user)
            carrito = Carrito.objects.get(usuario=request.user)
            
            productos = get_productos_from_carrito(carrito)

            if form.cleaned_data['forma_pago'] == FormaPago.CONTRARREEMBOLSO:
                
                create_pedido(request, datos_pedido, productos, estado=Estado.CONFIRMADO)
                
                carrito.limpiar_carrito()
                
                return render(request, 'exito_pago.html')

            elif form.cleaned_data['forma_pago'] == FormaPago.STRIPE:

                productos_stripe = []

                for item in carrito.items.all():
                    producto_info = {
                        'price_data': {
                            'currency': 'eur',
                            'product_data': {
                                'name': item.producto.nombre,
                            },
                            'unit_amount': int(item.producto.precio * 100),  # Monto en céntimos
                        },
                        'quantity': item.cantidad,
                    }
                    productos_stripe.append(producto_info)
                
                create_pedido(request, datos_pedido, productos)

                session = stripe.checkout.Session.create(
                    payment_method_types=['card'],
                    line_items=productos_stripe,
                    mode='payment',
                    success_url=request.build_absolute_uri(reverse('exito_pago_stripe')) + '?session_id={CHECKOUT_SESSION_ID}',
                    cancel_url=request.build_absolute_uri(reverse('cancelar_pago_stripe'))
                )

                return render(request, 'procesar_pago_stripe.html', {'session_id': session.id})

    else:
        form = DatosPagoForm()

    carrito, created = Carrito.objects.get_or_create(usuario=request.user)
    items = carrito.items.all()

    return render(request, 'procesar_pago.html', {'form': form, 'items': items})


def exito_pago_stripe(request):

    session_id = request.GET.get('session_id')

    if session_id:

        session = stripe.checkout.Session.retrieve(session_id)

        if session.payment_status == 'paid':

            ultimo_pedido = Pedido.objects.filter(usuario=request.user).order_by('-fecha_creacion').first()
            if ultimo_pedido:
                ultimo_pedido.estado = Estado.CONFIRMADO
                ultimo_pedido.save()

                carrito = Carrito.objects.get(usuario=request.user)
                carrito.limpiar_carrito()
                            
            else:
                return render(request, 'cancelar_pago.html')

            return render(request, 'exito_pago.html')


    return HttpResponse("PAGO NO EXITOSO")

def cancelar_pago_stripe(request):
    session_id = request.GET.get('session_id')
    return render(request, 'cancelar_pago.html')