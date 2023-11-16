from .models import Producto

def marcas(request):
    marcas_distintas = Producto.objects.values('marca').distinct()
    marcas = [marca['marca'] for marca in marcas_distintas]
    return {'marcas': marcas}