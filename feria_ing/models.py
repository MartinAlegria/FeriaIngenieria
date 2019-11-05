from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Project(models.Model):
    #KEY
    id = models.IntegerField(primary_key=True)
    nombre = models.CharField(max_length=140)
    descripcion = models.TextField()
    #FOREIGN KEY
    categoria = models.CharField(max_length=140)
    requierements = models.CharField(max_length=140)
    evaluaciones = models.IntegerField()

    def __str__(self):
        return self.nombre

class Evaluacion(models.Model):
    #KEY
    id_proyecto = models.ForeignKey(Project, on_delete = models.CASCADE)
    #FOREIGN KEY
    matricula = models.ForeignKey(User, on_delete = models.CASCADE)

    def __str__(self):
        return self.id_proyecto
