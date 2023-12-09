from math import prod
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.models import User
from cesta.models import Pedido
from producto.models import Producto
from datos_entrega.models import DatosEntrega
from django.db.models import Q, F, FloatField
from django.db.models.functions import Cast
from ProyectoPGPI.forms import ReclamacionForm, CustomUserCreationForm, UserProfileForm
from datos_entrega.forms import DatosEntregaForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import AuthenticationForm


def login2(request):
    if 'fake-' in request.user.username:
        logout(request)
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            try:
                usuario = User.objects.get(username=username)
                login(request, usuario)
            except User.DoesNotExist:
                form.add_error(None, "Usuario no existe")
        return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})
        
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
    query_oferta = Q()
    if busqueda_q:
        query &= Q(nombre__icontains = busqueda_q) | Q(descripcion__icontains = busqueda_q)
        query_oferta &= Q(nombre__icontains = busqueda_q) | Q(descripcion__icontains = busqueda_q)
    
    if busqueda_marca:
        query &= Q(marca__icontains=busqueda_marca)
        query_oferta &= Q(marca__icontains=busqueda_marca)
    
    if busqueda_precio_min:
        query &= Q(precio__gte=float(busqueda_precio_min))
        query_oferta &= Q(precio_rebajado__gte=float(busqueda_precio_min))
    
    if busqueda_precio_max:
        query &= Q(precio__lte=float(busqueda_precio_max))
        query_oferta = Q(precio_rebajado__lte=float(busqueda_precio_max))


    productos_rebajados = Producto.objects.annotate(
        precio_rebajado=Cast(F('precio') - (F('precio') * F('oferta__porcentaje') / 100), output_field=FloatField())
    ).filter(query_oferta).distinct()
    productos_originales = Producto.objects.filter(query).distinct()
    
    productos = productos_rebajados | productos_originales

    for producto in productos:
        if producto.nombre == 'Gastos de envío':
            productos = productos.exclude(nombre='Gastos de envío')
    if request.GET.get('q') != None or request.GET.get('q') or request.GET.get('marca') or request.GET.get('precio_min') or request.GET.get('precio_max'):
        return render(request, "lista_productos.html", {'productos': productos, 'marcas': marcas,'busqueda_q': busqueda_q, 'busqueda_marca': busqueda_marca, 'busqueda_precio_min': busqueda_precio_min, 'busqueda_precio_max': busqueda_precio_max})
    return render(request, 'home.html', {'productos': productos, 'marcas': marcas,'busqueda_q': busqueda_q, 'busqueda_marca': busqueda_marca, 'busqueda_precio_min': busqueda_precio_min, 'busqueda_precio_max': busqueda_precio_max})


def registro(request):
    data = {
        'form': CustomUserCreationForm()
    }
    if request.method == 'POST':
        if "fake-" in request.user.username:
            logout(request)
        user_creation_form = CustomUserCreationForm(data=request.POST)

        if user_creation_form.is_valid():
            user = user_creation_form.save()

            login(request, user)
            return redirect('home')
        else:
            data['mensaje'] = 'Ha habido un error en el formulario'
    return render(request, "registro.html", data)

@login_required
def cuenta(request):
    datos_entrega = DatosEntrega.objects.filter(user=request.user).first()
    
    if('fake-' in request.user.username) and request.user.is_authenticated:
        return redirect("registro")
    return render(request, 'cuenta.html', {'user': request.user, 'datos_entrega': datos_entrega})

@login_required
def logout_cuenta(request):
    logout(request)
    return redirect('home')

def obtener_producto(request, producto_id):
    try:
        producto = Producto.objects.get(id=producto_id)
        data = {'id': producto.id, 'nombre': producto.nombre, 'precio': producto.precio, 'precio_rebajado': producto.precio_rebajado()}
        return JsonResponse(data)
    except Producto.DoesNotExist:
        return JsonResponse({'error': 'Producto no encontrado'}, status=404)

@login_required
def editar_perfil(request):
    try:
        datos_entrega = DatosEntrega.objects.get(user=request.user)
    except DatosEntrega.DoesNotExist:
        datos_entrega = None

    if request.method == 'POST':
        user_form = UserProfileForm(request.POST, instance=request.user)
        datos_entrega_form = DatosEntregaForm(request.POST, instance=datos_entrega)

        if user_form.is_valid() and datos_entrega_form.is_valid():
            user_form.save()

            if datos_entrega_form.is_bound and datos_entrega is not None:
                datos_entrega_form.save()
            elif datos_entrega_form.is_bound and datos_entrega is None:
                # Si no hay datos_entrega existentes, crea uno nuevo
                datos_entrega_obj = datos_entrega_form.save(commit=False)
                datos_entrega_obj.user = request.user
                datos_entrega_obj.save()

            return redirect('cuenta')
    else:
        user_form = UserProfileForm(instance=request.user)
        datos_entrega_form = DatosEntregaForm(instance=datos_entrega)

    return render(request, 'editar_perfil.html', {'user_form': user_form, 'datos_entrega_form': datos_entrega_form})

@require_http_methods(["GET", "POST"]) 
def reclamaciones(request):
    if request.method == 'POST':
        reclamacion_creation_form = ReclamacionForm(data=request.POST)
        reclamacion_creation_form.save()
        return redirect('home')
    return render(request, 'reclamacion.html', {'form': ReclamacionForm()})

def seguimiento(request):
    pedido = None
    if request.method == 'POST':
        codigo = request.POST.get("codigo")
        pedidos = Pedido.objects.all()
        secretos = []
        for pedido in pedidos:
            secretos.append(pedido.secreto)
        if codigo in secretos:
            pedido = Pedido.objects.get(secreto=codigo)
        else:
            return redirect('seguimiento')

    return render(request, 'seguimiento.html', {'pedido':pedido})