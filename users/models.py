from django.db import models
from feria_ing import models as projects

class Alumno(models.Model):
    matricula = models.CharField(max_length=9,primary_key=True)
    nombres = models.CharField(max_length=140)
    apellidos = models.CharField(max_length=140)
    proyecto = models.OneToOneField(
        projects.Project,
        on_delete=models.SET_NULL,
        null = True
    )
    carrera = models.CharField(max_length=5)

    def __str__(self):
        return self.matricula

class Profesor(models.Model):
    matricula = models.CharField(max_length=9,primary_key=True)
    nombres = models.CharField(max_length=140)
    apellidos = models.CharField(max_length=140)

    def __str__(self):
        return self.matricula
