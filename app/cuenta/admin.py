from django.contrib import admin
from .models import *

class CuentaAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'uid',
        'cliente',
        'saldo'
        )

class MovimientoAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'cuenta',
        'importe',
        'tipo_movimiento'
        )

admin.site.register(Movimiento, MovimientoAdmin)
admin.site.register(Cuenta, CuentaAdmin)
