from django.shortcuts import get_object_or_404, render, redirect
from .forms import SearchForm

def home(request):
        return render(request, "home.html")
    
def buscador(request):
    form = SearchForm(request)
    resultados = []
    if request.method == 'POST':
        # Acceder directamente a los datos enviados en la solicitud
        query = request.POST.get('query', '')
        #resultados = perform_search(query)  aqui iria la funcion de buscador
    return render(request, 'busqueda.html', {'form': form, 'results': resultados})
    