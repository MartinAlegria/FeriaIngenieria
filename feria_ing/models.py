from django.db import models

# Create your models here.

class Categoria(models.Model):
    abreviacion = models.CharField(max_length=7, primary_key=True)
    nombre = models.CharField(max_length=100)
    num_proyectos = models.IntegerField()

    def __str__(self):
        return self.nombre

class Project(models.Model):
    #KEY
    id = models.IntegerField(primary_key=True)
    nombre = models.CharField(max_length=140)
    descripcion = models.TextField()
    #FOREIGN KEY
    categoria = models.OneToOneField(
        Categoria,
        on_delete = models.SET_NULL,
        null = True
    )
    requierements = models.CharField(max_length=140)
    evaluaciones = models.IntegerField()

    def __str__(self):
        return self.nombre