from django.contrib import admin
from .models import Oferta

@admin.register(Oferta)
class OfertaAdmin(admin.ModelAdmin):
    list_display = ['id', 'porcentaje']
    search_fields = ['porcentaje']


