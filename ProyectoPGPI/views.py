from django.shortcuts import get_object_or_404, render, redirect
from producto.models import Producto
from django.db.models import Q
from ProyectoPGPI.forms import CustomUserCreationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required


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
    print(request.GET.get('q'))
    if request.GET.get('q') != None or request.GET.get('q') or request.GET.get('marca') or request.GET.get('precio_min') or request.GET.get('precio_max'):
        return render(request, "lista_productos.html", {'productos': productos, 'marcas': marcas,'busqueda_q': busqueda_q, 'busqueda_marca': busqueda_marca, 'busqueda_precio_min': busqueda_precio_min, 'busqueda_precio_max': busqueda_precio_max})
    return render(request, 'home.html', {'productos': productos, 'marcas': marcas,'busqueda_q': busqueda_q, 'busqueda_marca': busqueda_marca, 'busqueda_precio_min': busqueda_precio_min, 'busqueda_precio_max': busqueda_precio_max})


def registro(request):
    data = {
        'form': CustomUserCreationForm()
    }
    if request.method == 'POST':
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
    return render(request, "cuenta.html", {'user': request.user})

@login_required
def logout_cuenta(request):
    logout(request)
    return redirect('home')

