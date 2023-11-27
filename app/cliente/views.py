from .models import Cliente, Categoria
from rest_framework import viewsets, mixins
from .serializers import ClienteSerializer
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404

class ClienteViewSet(viewsets.ModelViewSet):
    """
    Vista que permite crear, eliminar,
    actualizar, obtener y listar clientes
    """
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer

    @action(detail=True, methods=['post'])
    def agregar_categoria(self, request, pk=None):
        """
        Permite agregar una categoria a un
        cliente especifico 
        """
        cliente_instance = self.get_object()
        categoria_id = request.data.get('categoria_id',None)
        categoria_instance = get_object_or_404(RapiUser, pk=categoria_id)
        cliente.categorias.add(categoria_instance)
        serializer = self.get_serializer_class()
        data = serializer(cliente_instance).data
        return Response(data)

        
        