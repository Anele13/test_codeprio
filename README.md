# Proyecto de gestión de Cuentas y Clientes en Django

Este es un proyecto hecho en Django que implementa un sistema de gestión de clientes, cuentas y movimientos con las siguientes funcionalidades:

Clientes
- Crear, ver, actualizar y eliminar clientes
- Listar todos los clientes
- Agregar cliente a categoría
- Consultar un cliente, sus cuentas y categorías
- Consultar saldo (*) disponible en cada una de sus cuentas

Movimientos
- Registrar un movimiento (puede ser del tipo Ingreso o Egreso de dinero)
- Eliminar un movimiento
- Consultar un movimiento

## Herramientas Utilizadas

- Django 4.2.5
- drf-spectacular 0.24.1
- djangorestframework 3.14.0
- PyMemcache
- Docker Compose

## Instalación

1. Clonar este repositorio

2. Construir con docker:

- ```docker-compose up --build```

3. Inicializar la base con datos:

- ```python manage.py loaddata categorias.json```
- ```python manage.py loaddata clientes.json```
- ```python manage.py loaddata cuentas.json```

## API y DOCS

- Documentación OpenAPI disponible en: http://localhost:8000/api/docs

## TEST

- Para correr test correr el comando:
- ```docker-compose exec app python manage.py test```