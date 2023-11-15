from django.shortcuts import get_object_or_404, render, redirect
from ProyectoPGPI.forms import CustomUserCreationForm
from producto.models import Producto
from django.db.models import Q
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required


def home(request):
    busqueda = request.GET.get('buscar')
    if busqueda:
        productos = Producto.objects.filter(
            Q(nombre__icontains = busqueda) |
            Q(modelo__icontains = busqueda)
        ).distinct
        return render(request, "lista_productos.html", {'productos': productos})
    return render(request, "home.html")

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

    


