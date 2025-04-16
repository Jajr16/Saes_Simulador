from django.db import models

class Alumno(models.Model):
    boleta = models.CharField(max_length=50, unique=True)  # Campo para almacenar la boleta
    imagen_credencial = models.URLField(max_length=200, blank=True, null=True)  # URL de la foto del alumno
    
    # Otros campos que puedas necesitar para el alumno
    nombre = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)

    def __str__(self):
        return self.boleta  # Devuelve la boleta al imprimir el objeto
