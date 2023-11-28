from .models import Movimiento
from rest_framework import viewsets, mixins
from .serializers import MovimientoSerializer, MovimientoCreateSerializer
from .exceptions import MovimientoException
from rest_framework.exceptions import APIException
from rest_framework import status

class MovimientoViewSet(mixins.CreateModelMixin,
                        mixins.DestroyModelMixin,
                        mixins.RetrieveModelMixin,
                        viewsets.GenericViewSet):
    """
    Vista que permite crear, eliminar 
    y obtener un movimiento de cuenta
    """
    queryset = Movimiento.objects.all()
    serializer_class = MovimientoSerializer

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return MovimientoCreateSerializer
        return self.serializer_class

    def perform_destroy(self, instance):
        try:
            return Movimiento.remove(instance)
        except MovimientoException as e:
            exception = APIException(str(e))
            exception.status_code = status.HTTP_400_BAD_REQUEST
            raise exception