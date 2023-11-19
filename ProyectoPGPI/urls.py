"""
URL configuration for ProyectoPGPI project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from producto.views import lista_productos, detalles_producto
from .views import home, obtener_producto, registro, cuenta, logout_cuenta


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('productos/', lista_productos, name='lista_productos'),
    path('productos/<int:producto_id>/', detalles_producto, name='detalles_producto'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/register/', registro, name="registro"),
    path('cuenta/', cuenta, name='cuenta'),
    path('logout/', logout_cuenta, name='logout'),
    path('obtener_producto/<int:producto_id>/', obtener_producto),
    path('autocaravana/<int:producto_id>/', detalles_producto, name='detalles_producto'),

    

]

for module in settings.MODULES:
    urlpatterns += [
        path('{}/'.format(module), include('{}.urls'.format(module)))
    ]