from django.db import models

class Categoria(models.Model):
    """
    Modelo para representar una categoria de cliente
    """
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre

class Cliente(models.Model):
    """
    Modelo para representar un cliente 
    """
    nombre = models.CharField(max_length=100)
    categorias = models.ManyToManyField(Categoria)

    def __str__(self):
        return self.nombre
