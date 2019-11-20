from django.db import models
from feria_ing.models import (Project)

class Alumno(models.Model):
    matricula = models.CharField(max_length=25,primary_key=True)
    nombres = models.CharField(max_length=140)
    apellidos = models.CharField(max_length=140)
    proyecto = models.ForeignKey(Project,on_delete=models.CASCADE, null =True)
    carrera = models.CharField(max_length=5)

    def __str__(self):
        return self.matricula

class Profesor(models.Model):
    matricula = models.CharField(max_length=29,primary_key=True)
    nombres = models.CharField(max_length=140)
    apellidos = models.CharField(max_length=140)
    profe = models.BooleanField(default=False)

    def __str__(self):
        return self.matricula

class Evaluacion(models.Model):
    proyecto = models.ForeignKey(
        Project,
        on_delete = models.CASCADE,
        null = False,
        default = None
    )
    profesor = models.ForeignKey(
        Profesor,
        on_delete = models.CASCADE,
        null = False,
        default = None
    )
    calificacion = models.IntegerField(null=False, default= None)