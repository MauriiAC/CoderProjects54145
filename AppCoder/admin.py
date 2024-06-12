from django.contrib import admin
from datetime import datetime
from .models import *

class CursoAdmin(admin.ModelAdmin):
  list_display = ['nombre', 'camada']
  search_fields = ['nombre', 'camada']
  list_filter = ['nombre']

class EntregableAdmin(admin.ModelAdmin):
  list_display = ["nombre", "fechaDeEntrega", "entregado", "antiguedad"]

  def antiguedad(self, object):
    if object.fechaDeEntrega:
      return (datetime.now().date() - object.fechaDeEntrega).days

# Register your models here.
admin.site.register(Curso, CursoAdmin)
admin.site.register(Profesor)
admin.site.register(Estudiante)
admin.site.register(Entregable, EntregableAdmin)
admin.site.register(Avatar)

