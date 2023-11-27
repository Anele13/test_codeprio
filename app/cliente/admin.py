from django.contrib import admin
from .models import *

class ClienteAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'nombre',
        )

admin.site.register(Cliente, ClienteAdmin)
admin.site.register(Categoria)

