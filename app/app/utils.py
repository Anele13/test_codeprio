from rest_framework import status
import requests
from decimal import Decimal
from django.core.cache import cache
from django.conf import settings
import logging

class DolarsiAPI():
    """
    Clase utilizada para obterner precios de dolar
    actualizados
    """
    API_URL = 'https://www.dolarsi.com/api/api.php?type=valoresprincipales'

    @classmethod
    def call_api(cls, tipo_dolar):
        valor = 0
        try:
            request = requests.get(cls.API_URL)
            if request.status_code == status.HTTP_200_OK:
                json = request.json()
                valor = Decimal(
                    list(
                        filter(lambda d: d['casa']['nombre'] == tipo_dolar, json)
                    )[0]['casa']['venta'].replace(',','.')
                )
        except Exception as e:
            logger = logging.getLogger(__name__)
            logger.exception(f"Error en dolarsi API: {e}")
        return valor


    @classmethod
    def get_cotizacion_actual(cls, tipo_dolar):
        """ 
        Dado un tipo de dolar (Soja, Blue, etc)
        devuelve su correspondiente cotizacion actual
        """
        cache_key = 'cotizacion_dolar'
        cache_time = settings.CACHE_DOLARAPI_EXPIRE_TIME
        monto = cache.get(cache_key, None) 
        if not monto:
            monto = cls.call_api(tipo_dolar)
            cache.set(cache_key, monto, cache_time)
        return monto
        