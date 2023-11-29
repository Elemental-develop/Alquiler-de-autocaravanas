from django.contrib import admin
from claim.models import Claim

@admin.register(Claim)
class ClaimAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'descripcion']
    search_fields = ['titulo']