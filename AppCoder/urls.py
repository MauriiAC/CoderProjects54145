from django.urls import path
from AppCoder.views import (
  curso, 
  lista_cursos, 
  inicio, 
  cursos, 
  profesores, 
  estudiantes, 
  entregables,
  curso_formulario,
  busqueda_camada,
  buscar
)

urlpatterns = [
    path('agrega-curso/<nombre>/<camada>', curso),
    path('lista-cursos/', lista_cursos),
    path('', inicio, name='Inicio'),
    path('cursos/', cursos, name='Cursos'),
    path('profesores/', profesores, name='Profesores'),
    path('estudiantes/', estudiantes, name='Estudiantes'),
    path('entregables/', entregables, name='Entregables'),
    path('curso-formulario/', curso_formulario, name='CursoFormulario'),
    path('busqueda-camada/', busqueda_camada, name='BusquedaCamada'),
    path('buscar/', buscar, name='BuscarCurso'),
]
