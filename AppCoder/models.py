from django.db import models

# Create your models here.
class Curso(models.Model):

  nombre = models.CharField(max_length=40)
  camada = models.IntegerField()

  def __str__(self):
    return f'{self.nombre} - {self.camada}'
  
  class Meta():

    verbose_name = 'Course'
    verbose_name_plural = 'The courses'
    ordering = ('nombre', 'camada')
    unique_together = ('nombre', 'camada')

class Estudiante(models.Model):

  nombre = models.CharField(max_length=30)
  apellido = models.CharField(max_length=30)
  email = models.EmailField(null=True)

  def __str__(self):
    return f'{self.nombre} - {self.apellido}'

class Profesor(models.Model):

  nombre = models.CharField(max_length=30)
  apellido = models.CharField(max_length=30)
  email = models.EmailField()
  profesion = models.CharField(max_length=30)
  cursos = models.ManyToManyField(Curso)

  def __str__(self):
    return f'{self.nombre} {self.apellido}'  

class Entregable(models.Model):

  nombre = models.CharField(max_length=30)
  fechaDeEntrega = models.DateField()
  entregado = models.BooleanField()
  estudiante = models.ForeignKey(Estudiante, on_delete=models.CASCADE)