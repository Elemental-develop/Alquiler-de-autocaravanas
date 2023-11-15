from django.shortcuts import get_object_or_404, render, redirect


def buscador(request):
    resultados = []
    if request.method == 'POST':
        # Acceder directamente a los datos enviados en la solicitud
        query = request.POST.get('query', '')
        #resultados = perform_search(query)  aqui iria la funcion de buscador
    return render(request, 'busqueda.html', { 'results': resultados})
    