from django.db import models

# Create your models here.
class Proyecto(models.Model):
    id = models.IntegerField(primary_key=True)
    nombre = models.CharField(max_length=255)
    tipo = models.CharField(max_length=50)
    region = models.CharField(max_length=50)
    tipologia = models.CharField(max_length=50)
    titular = models.CharField(max_length=255)
    inversion = models.DecimalField(max_digits=10, decimal_places=4)
    ingreso = models.DateField()
    estado = models.CharField(max_length=50)
