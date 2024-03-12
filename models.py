from django.db import models
# Create your models here.
class Sistema(models.Model):
    nombre = models.CharField(max_length=255)
    salario = models.DecimalField(decimal_places=6, max_digits=21)

