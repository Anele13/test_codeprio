from django.db import models
from cliente.models import Cliente
from .exceptions import SaldoInsuficienteException
from app.utils import DolarsiAPI
import uuid
from django.db import transaction
from django.core.validators import MinValueValidator
from decimal import Decimal

class Cuenta(models.Model):
    """ 
    Modelo para representar una cuenta de 
    un cliente
    """
    uid = models.UUIDField(
        unique=True,
        editable=False,
        default=uuid.uuid4,
        verbose_name='ID publico',
    )
    cliente = models.ForeignKey(
        Cliente,
        on_delete=models.PROTECT,
        related_name='cuentas'
    )
    saldo = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        default=0,
        validators=[MinValueValidator(Decimal('0'))],
    )

    class Meta:
        constraints = [
            models.constraints.CheckConstraint(
                check=models.Q(saldo__gte=Decimal('0')),
                name='saldo_positivo'
            )
        ]

    def __str__(self):
        return f'Cuenta del cliente {self.cliente} - {self.uid}'

    def get_total_usd(self):
        tipo_dolar = 'Dolar Bolsa'
        cotizacion_dolar = DolarsiAPI.get_cotizacion_actual(tipo_dolar)
        return self.saldo * cotizacion_dolar

class Movimiento(models.Model):
    """
    Modelo para representar los movimientos
    de una cuenta
    """
    INGRESO = 1
    EGRESO = 2
    TIPO_MOVIMIENTO_CHOICES = (
        (INGRESO, 'Ingreso'),
        (EGRESO, 'Egreso')
    )
    cuenta = models.ForeignKey(
        Cuenta,
        on_delete=models.PROTECT,
        related_name='movimientos'
    )
    fecha_creacion = models.DateTimeField(
        auto_now_add=True
    )
    tipo_movimiento = models.IntegerField(
        choices=TIPO_MOVIMIENTO_CHOICES
    )
    importe = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        default=0,
        validators=[MinValueValidator(Decimal('0'))],
    )

    class Meta:
        constraints = [
            models.constraints.CheckConstraint(
                check=models.Q(importe__gte=Decimal('0')),
                name='importe_positivo'
            )
        ]

    def __str__(self):
        return f'Movimiento: {self.get_tipo_movimiento_display()} - {self.importe}'

    @classmethod
    def create(cls, data):
        cuenta = data.get('cuenta')
        importe = data.get('importe')
        tipo_movimiento = data.get('tipo_movimiento')
        with transaction.atomic():
            cuenta = Cuenta.objects.select_for_update().get(id=cuenta.id)
            if tipo_movimiento == cls.INGRESO:
                cuenta.saldo += importe
            else:
                if importe > cuenta.saldo:
                    raise SaldoInsuficienteException(cuenta.saldo)
                cuenta.saldo -= importe
            cuenta.save(update_fields=['saldo'])
            return cls.objects.create(**data)

    @classmethod
    def delete(cls, movimiento_object):
        with transaction.atomic():
            cuenta = Cuenta.objects.select_for_update().get(id=movimiento_object.cuenta_id)
            if movimiento_object.tipo_movimiento == cls.INGRESO:
                if movimiento_object.importe > cuenta.saldo:
                    raise SaldoInsuficienteException(cuenta.saldo)
                cuenta.saldo -= movimiento_object.importe
            else:
                cuenta.saldo -= movimiento_object.importe
            cuenta.save(update_fields=['saldo'])
            return movimiento_object.delete()