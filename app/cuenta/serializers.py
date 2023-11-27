from rest_framework import serializers
from .models import Movimiento, Cuenta

class MovimientoCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movimiento
        fields = (
            'id',
            'cuenta',
            'tipo_movimiento',
            'importe'
        )
    

class MovimientoSerializer(serializers.ModelSerializer):
    tipo_movimiento = serializers.SerializerMethodField()
    cuenta = serializers.SerializerMethodField()

    class Meta:
        model = Movimiento
        fields = (
            'id',
            'cuenta',
            'fecha_creacion',
            'tipo_movimiento',
            'importe'
        )
    
    def get_tipo_movimiento(self, instancia):
        return instancia.get_tipo_movimiento_display()

    def get_cuenta(self, instancia):
        return instancia.cuenta.uid

class CuentaSerializer(serializers.ModelSerializer):
    saldo_usd = serializers.SerializerMethodField()

    class Meta:
        model = Cuenta
        fields = (
            'uid',
            'saldo',
            'saldo_usd'
        )
    
    def get_saldo_usd(self, instancia):
        return instancia.get_total_usd()