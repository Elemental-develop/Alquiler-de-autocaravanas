from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

class ClienteAdmin(UserAdmin):
    list_display = ['username', 'email', 'first_name', 'last_name']

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(is_superuser=False)

admin.site.unregister(User)
admin.site.register(User, ClienteAdmin)