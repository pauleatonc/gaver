from django.db import models

class Textos(models.Model):
    nombre = models.CharField(max_length=200)
    texto = models.TextField(max_length=2000)

    def __str__(self):
        return self.nombre
