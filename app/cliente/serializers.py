from rest_framework import serializers
from .models import Cliente, Categoria
from cuenta.serializers import CuentaSerializer

class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = (
            'nombre',
        )

class ClienteSerializer(serializers.ModelSerializer):
    categorias = CategoriaSerializer(many=True, read_only=True)
    cuentas = CuentaSerializer(many=True, read_only=True)

    class Meta:
        model = Cliente
        fields = (
            'id',
            'nombre',
            'categorias',
            'cuentas'
        )