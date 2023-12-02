from django.shortcuts import render

from producto.forms import OpinionForm
from .models import Producto
from oferta.models import Oferta

from django.shortcuts import render, get_object_or_404

def lista_productos(request):
        
    categoria = request.GET.get('categoria', '')
    productos = Producto.objects.all()
    
    if categoria != '':
        productos = Producto.objects.filter(categoria=categoria)
    for producto in productos:
        if producto.nombre == 'Gastos de envío':
            productos = productos.exclude(nombre='Gastos de envío')

    return render(request, 'lista_productos.html', {'productos': productos})




def detalles_producto(request, producto_id):
    productos = Producto.objects.all()
    producto_seleccionado = get_object_or_404(Producto, pk=producto_id)
    lista_opiniones = []
    lista_usuarios = []

    for opinion in producto_seleccionado.opiniones.split(','):
        if ';*' in opinion:
            usuario = opinion.split(';*')[1]
        else:
            usuario = 'Anónimo'

        opinion_actual = opinion.split(';*')[0]
        lista_opiniones.append(opinion_actual)
        lista_usuarios.append(usuario)

    if request.method == 'POST':
        form = OpinionForm(request.POST)
        if form.is_valid():
            nueva_opinion = form.cleaned_data['opinion']
            if request.user.is_authenticated:
                nueva_opinion = f'{nueva_opinion};*{request.user.username}'
            producto_seleccionado.agregar_opinion(nueva_opinion)

            print(nueva_opinion)
            if ';*' in nueva_opinion:
                usuario = nueva_opinion.split(';*')[1]
            else:
                usuario = 'Anónimo'
            print(usuario)
            lista_usuarios.append(usuario)
            nueva_opinion = nueva_opinion.split(';*')[0]
            lista_opiniones.append(nueva_opinion)
    else:
        form = OpinionForm()
    
    if len(lista_opiniones) > 1:
        lista_opiniones.__delitem__(1)
        lista_opiniones.__delitem__(0)
    if len(lista_usuarios) > 1:
        lista_usuarios.__delitem__(1)
        lista_usuarios.__delitem__(0)

    usuarios_opiniones = list(zip(lista_usuarios, lista_opiniones))
    
    return render(request, 'detalles_producto.html', {'productos': productos, 'producto_seleccionado': producto_seleccionado, 'opinion_form': form, 'opiniones': lista_opiniones, 'usuarios': lista_usuarios, 'usuarios_opiniones': usuarios_opiniones})
   

