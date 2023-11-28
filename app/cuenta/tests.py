from django.test import TestCase
from rest_framework import status
from django.urls import reverse
from rest_framework.test import APIClient
from .models import Cuenta, Movimiento
from cliente.models import Cliente
class MovimientoTestCase(TestCase):
    MOVIMIENTO_URL = '/movimiento/'

    def setUp(self):
        self.client = APIClient()

    def test_crear_movimiento(self):
        #---------------------------- INGRESO ------------------------------
        cliente = Cliente.objects.create(nombre='Pedro')
        cuenta = Cuenta.objects.create(cliente=cliente)
        data = {
            "cuenta": cuenta.id, 
            "tipo_movimiento": Movimiento.INGRESO,
            "importe": 100
        }
        #Crear movimiento de INGRESO sobre cuenta existente
        response = self.client.post(self.MOVIMIENTO_URL, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        cuenta.refresh_from_db()
        self.assertEqual(cuenta.saldo, 100)

        #Crear movimiento de INGRESO sobre cuenta inexistente
        data['cuenta'] = 999
        response = self.client.post(self.MOVIMIENTO_URL, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        #Crear movimiento de INGRESO con monto negativo
        data['importe'] = -100
        response = self.client.post(self.MOVIMIENTO_URL, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        #Crear movimiento de INGRESO con tipo movimiento inexistente
        data['tipo_movimiento'] = 999
        response = self.client.post(self.MOVIMIENTO_URL, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        #---------------------------- EGRESO ------------------------------------
        cuenta2 = Cuenta.objects.create(cliente=cliente)
        data = {
            "cuenta": cuenta2.id, 
            "tipo_movimiento": Movimiento.EGRESO,
            "importe": 100,
        }

        #Ingresar monto y retirarlo
        data['tipo_movimiento'] = Movimiento.INGRESO
        response = self.client.post(self.MOVIMIENTO_URL, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        cuenta2.refresh_from_db()
        self.assertEqual(cuenta2.saldo, 100)

        data['tipo_movimiento'] = Movimiento.EGRESO
        response = self.client.post(self.MOVIMIENTO_URL, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        cuenta2.refresh_from_db()
        self.assertEqual(cuenta2.saldo, 0)

        #Crear movimiento de EGRESO sobre cuenta inexistente
        data['cuenta'] = 999
        response = self.client.post(self.MOVIMIENTO_URL, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        #Crear movimiento de EGRESO con cuenta en saldo 0
        data['importe'] = 100
        cuenta2.refresh_from_db()
        self.assertEqual(cuenta2.saldo, 0)
        response = self.client.post(self.MOVIMIENTO_URL, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        #Crear movimiento de EGRESO con monto negativo
        data['importe'] = -100
        response = self.client.post(self.MOVIMIENTO_URL, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        #Crear movimiento de EGRESO con tipo movimiento inexistente
        data['tipo_movimiento'] = 999
        response = self.client.post(self.MOVIMIENTO_URL, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_eliminar_movimiento(self):
        #Eliminar movimiento inexistente
        movimiento_id = 999
        self.assertEqual(Movimiento.objects.filter(id=movimiento_id).exists(), False)
        response = self.client.delete(f'{self.MOVIMIENTO_URL}{movimiento_id}/', format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        #Crear movimiento de INGRESO sobre cuenta existente
        cliente = Cliente.objects.create(nombre='Pedro')
        cuenta3 = Cuenta.objects.create(cliente=cliente)
        data = {
            "cuenta": cuenta3.id, 
            "tipo_movimiento": Movimiento.INGRESO,
            "importe": 100
        }
        response = self.client.post(self.MOVIMIENTO_URL, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        cuenta3.refresh_from_db()
        self.assertEqual(cuenta3.saldo, 100)

        #Eliminar el movimiento de ingreso
        resp = response.json()
        movimiento_id = resp.get('id')
        response = self.client.delete(f'{self.MOVIMIENTO_URL}{movimiento_id}/', format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        cuenta3.refresh_from_db()
        self.assertEqual(cuenta3.saldo, 0)

        #----------------------------------------
        #Crear movimiento de INGRESO sobre cuenta existente
        cuenta4 = Cuenta.objects.create(cliente=cliente)
        data = {
            "cuenta": cuenta4.id, 
            "tipo_movimiento": Movimiento.INGRESO,
            "importe": 100
        }
        response = self.client.post(self.MOVIMIENTO_URL, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        cuenta4.refresh_from_db()
        self.assertEqual(cuenta4.saldo, 100)
        
        # Creo movimiento de egreso
        data['tipo_movimiento'] = Movimiento.EGRESO
        response = self.client.post(self.MOVIMIENTO_URL, data, format='json')
        resp = response.json()
        movimiento_id = resp.get('id')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        cuenta4.refresh_from_db()
        self.assertEqual(cuenta4.saldo, 0)

        #Eliminar el movimiento de egreso
        response = self.client.delete(f'{self.MOVIMIENTO_URL}{movimiento_id}/', format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        cuenta4.refresh_from_db()
        self.assertEqual(cuenta4.saldo, 100)