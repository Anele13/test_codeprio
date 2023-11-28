from django.test import TestCase
from .models import Cliente, Categoria
from rest_framework import status
from django.urls import reverse
from rest_framework.test import APIClient


class ClienteTestCase(TestCase):
    CLIENTE_URL = '/cliente/'

    def setUp(self):
        self.client = APIClient()
        self.categoria = Categoria.objects.create(nombre='Categoria Test')

    def test_crear_cliente(self):
        # Caso positivo: Crear un cliente correctamente
        data = {'nombre': 'Pedro'}
        response = self.client.post(self.CLIENTE_URL, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Caso erróneo: Intentar crear un cliente sin nombre
        data = {'nombre': ''}
        response = self.client.post(self.CLIENTE_URL, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_ver_actualizar_eliminar_cliente(self):
        # Crear un cliente para las pruebas de ver, actualizar y eliminar
        cliente = Cliente.objects.create(nombre='Cliente Test')

        # Caso positivo: Ver un cliente existente
        response = self.client.get(f'{self.CLIENTE_URL}{cliente.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Caso positivo: Actualizar el nombre de un cliente
        data = {'nombre': 'Nuevo Nombre'}
        response = self.client.patch(f'{self.CLIENTE_URL}{cliente.id}/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        cliente.refresh_from_db()
        self.assertEqual(cliente.nombre, 'Nuevo Nombre')

        # Caso erróneo: Intentar actualizar un cliente con nombre vacío
        data = {'nombre': ''}
        response = self.client.put(f'{self.CLIENTE_URL}{cliente.id}/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Caso positivo: Eliminar un cliente existente
        response = self.client.delete(f'{self.CLIENTE_URL}{cliente.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_listar_clientes(self):
        # Crear clientes para probar la lista de clientes
        Cliente.objects.create(nombre='Cliente1')
        Cliente.objects.create(nombre='Cliente2')

        # Caso positivo: Listar todos los clientes
        response = self.client.get(self.CLIENTE_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_agregar_categoria_a_cliente(self):
        cliente = Cliente.objects.create(nombre='Cliente Test')
        categorias_existentes = cliente.categorias.count()
        # Caso positivo: Agregar un cliente a una categoría existente
        data = {'categoria_id': self.categoria.id}
        response = self.client.post(f'{self.CLIENTE_URL}{cliente.id}/agregar_categoria/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        cliente.refresh_from_db()
        self.assertEqual(cliente.categorias.count(), categorias_existentes + 1)

        # Caso erróneo: Intentar agregar un cliente a una categoría inexistente
        categorias_existentes = cliente.categorias.count()
        data = {'categoria_id': 999} #Categoria inexistente
        response = self.client.post(f'{self.CLIENTE_URL}{cliente.id}/agregar_categoria/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        cliente.refresh_from_db()
        self.assertEqual(cliente.categorias.count(), categorias_existentes)