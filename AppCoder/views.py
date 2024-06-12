from typing import Any
from django.db.models.query import QuerySet
from django.http import HttpResponse
from django.shortcuts import render
from .models import Curso, Profesor, Avatar
from .forms import CursoFormulario, ProfesorFormulario, UserEditForm, AvatarFormulario
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import DeleteView, UpdateView, CreateView
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect

# Create your views here.
def curso(req, nombre, camada):

  nuevo_curso = Curso(nombre=nombre, camada=camada)
  nuevo_curso.save()

  return HttpResponse(f"""
    <p>Curso: {nuevo_curso.nombre} - Camada: {nuevo_curso.camada} creado!</p>
  """)

@staff_member_required(login_url="/app-coder/login")
def lista_cursos(req):

  lista = Curso.objects.all()

  return render(req, "lista_cursos.html", {"lista_cursos": lista})

def inicio(req):

  try:
    avatar = Avatar.objects.get(user=req.user.id)
    return render(req, "inicio.html", {"url": avatar.imagen.url})
  except:
    return render(req, "inicio.html")


def cursos(req, start=0):

  cant_por_pagina = 3

  if req.GET.get('direction') == 'next':
    start += 1
  elif req.GET.get('direction') == 'previous':
    start -= 1

  inicio = int(start)*cant_por_pagina
  final = (int(start)+1)*cant_por_pagina
  lista = Curso.objects.all()[inicio:final]

  return render(req, "cursos.html", {"lista_cursos": lista, "current_page": start})

def profesores(req):

  return render(req, "profesores.html", {})

def estudiantes(req):

  return render(req, "estudiantes.html", {})

def entregables(req):

  return render(req, "entregables.html", {})

def curso_formulario(req):

  print('method: ', req.method)
  print('POST: ', req.POST)

  if req.method == 'POST':

    miFormulario = CursoFormulario(req.POST)

    if miFormulario.is_valid():

      data = miFormulario.cleaned_data

      nuevo_curso = Curso(nombre=data['nombre'], camada=data['camada'])
      nuevo_curso.save()

      return render(req, "inicio.html", {"message": "Curso creado con éxito"})
    
    else:

      return render(req, "inicio.html", {"message": "Datos inválidos"})
  
  else:

    miFormulario = CursoFormulario()

    return render(req, "curso_formulario.html", {"miFormulario": miFormulario})


def busqueda_camada(req):

    return render(req, "busqueda_camada.html", {})

def buscar(req):

  if req.GET["camada"]:

    camada = req.GET["camada"]

    cursos = Curso.objects.filter(camada__icontains=camada)

    return render(req, "resultadoBusqueda.html", {"cursos": cursos, "camada": camada})

  else:
      
      return render(req, "inicio.html", {"message": "No envias el dato de la camada"})

def lista_profesores(req):

  try:

    if req.user.profesor:

      mis_profesores = Profesor.objects.all()

      return render(req, "leer_profesores.html", {"profesores": mis_profesores})
    
    else:

      return HttpResponseRedirect('/app-coder/')

  except:

      return HttpResponseRedirect('/app-coder/')


def crea_profesor(req):

  if req.method == 'POST':

    info = req.POST

    miFormulario = ProfesorFormulario({
      "nombre": info["nombre"],
      "apellido": info["apellido"],
      "email": info["email"],
      "profesion": info["profesion"],
    })

    userForm = UserCreationForm({
      "username": info["username"],
      "password1": info["password1"],
      "password2": info["password2"],
    })

    if miFormulario.is_valid() and userForm.is_valid():

      data = miFormulario.cleaned_data

      data.update(userForm.cleaned_data)

      user = User(username=data["username"])
      user.set_password(data["password1"])
      user.save()

      nuevo_profesor = Profesor(nombre=data['nombre'], apellido=data['apellido'], email=data['email'], profesion=data['profesion'], user_id=user)
      nuevo_profesor.save()

      return render(req, "inicio.html", {"message": "Profesor creado con éxito"})
    
    else:

      return render(req, "inicio.html", {"message": "Datos inválidos"})
  
  else:

    miFormulario = ProfesorFormulario()
    userForm = UserCreationForm()
    

    return render(req, "profesor_formulario.html", {"miFormulario": miFormulario, "userForm": userForm})
  
def eliminar_profesor(req, id):

  if req.method == 'POST':

    profesor = Profesor.objects.get(id=id)
    profesor.delete()

    mis_profesores = Profesor.objects.all()

  return render(req, "leer_profesores.html", {"profesores": mis_profesores})

def editar_profesor(req, id):

  if req.method == 'POST':

    miFormulario = ProfesorFormulario(req.POST)

    if miFormulario.is_valid():

      data = miFormulario.cleaned_data
      profesor = Profesor.objects.get(id=id)

      profesor.nombre = data["nombre"]
      profesor.apellido = data["apellido"]
      profesor.email = data["email"]
      profesor.profesion = data["profesion"]

      profesor.save()

      return render(req, "inicio.html", {"message": "Profesor actualizado con éxito"})
    
    else:

      return render(req, "inicio.html", {"message": "Datos inválidos"})
  
  else:

    profesor = Profesor.objects.get(id=id)

    miFormulario = ProfesorFormulario(initial={
      "nombre": profesor.nombre,
      "apellido": profesor.apellido,
      "email": profesor.email,
      "profesion": profesor.profesion,
    })

    return render(req, "editar_profesor.html", {"miFormulario": miFormulario, "id": profesor.id})
  

class CursoList(LoginRequiredMixin, ListView):

  model = Curso
  template_name = 'curso_list.html'
  context_object_name = "cursos"

  def get_queryset(self):
    profesor_email = self.kwargs.get("profesor_email")
    profesor = Profesor.objects.get(email=profesor_email)
    
    return profesor.cursos.all()

class CursoDetail(DetailView):

  model = Curso
  template_name = 'curso_detail.html'
  context_object_name = "curso"

class CursoCreate(CreateView):

  model = Curso
  template_name = 'curso_create.html'
  fields = ["nombre", "camada"]
  success_url = "/app-coder/"

class CursoUpdate(UpdateView):

  model = Curso
  template_name = 'curso_update.html'
  fields = ('__all__')
  success_url = "/app-coder/"
  context_object_name = "curso"

class CursoDelete(DeleteView):

  model = Curso
  template_name = 'curso_delete.html'
  success_url = "/app-coder/"
  context_object_name = "curso"

def login_view(req):

  if req.method == 'POST':

    miFormulario = AuthenticationForm(req, data=req.POST)

    if miFormulario.is_valid():

      data = miFormulario.cleaned_data

      usuario = data["username"]
      psw = data["password"]

      user = authenticate(username=usuario, password=psw)

      if user:
        login(req, user)
        return render(req, "inicio.html", {"message": f"Bienvenido {usuario}"})
      
      else:
        return render(req, "inicio.html", {"message": "Datos erroneos"})
    
    else:

      return render(req, "inicio.html", {"message": "Datos inválidos"})
  
  else:

    miFormulario = AuthenticationForm()

    return render(req, "login.html", {"miFormulario": miFormulario})
  

def register(req):

  if req.method == 'POST':

    miFormulario = UserCreationForm(req.POST)

    if miFormulario.is_valid():

      data = miFormulario.cleaned_data

      usuario = data["username"]
      miFormulario.save()
      
      return render(req, "inicio.html", {"message": f"Usuario {usuario} creado con éxito!"})
    
    else:

      return render(req, "inicio.html", {"message": "Datos inválidos"})
  
  else:

    miFormulario = UserCreationForm()

    return render(req, "registro.html", {"miFormulario": miFormulario})
  
@login_required()
def editar_perfil(req):

  usuario = req.user

  if req.method == 'POST':

    miFormulario = UserEditForm(req.POST, instance=req.user)

    if miFormulario.is_valid():

      data = miFormulario.cleaned_data

      usuario.first_name = data["first_name"]
      usuario.last_name = data["last_name"]
      usuario.email = data["email"]
      usuario.set_password(data["password1"])

      usuario.save()

      return render(req, "inicio.html", {"message": "Datos actualizado con éxito"})
    
    else:

      return render(req, "editar_perfil.html", {"miFormulario": miFormulario})
  
  else:

    miFormulario = UserEditForm(instance=req.user)

    return render(req, "editar_perfil.html", {"miFormulario": miFormulario})
  

def agregar_avatar(req):

  if req.method == 'POST':

    miFormulario = AvatarFormulario(req.POST, req.FILES)

    if miFormulario.is_valid():

      data = miFormulario.cleaned_data

      avatar = Avatar(user=req.user, imagen=data["imagen"])
      avatar.save()

      return render(req, "inicio.html", {"message": "Avatar cargado con éxito"})
    
    else:

      return render(req, "inicio.html", {"message": "Datos inválidos"})
  
  else:

    miFormulario = AvatarFormulario()

    return render(req, "agregar_avatar.html", {"miFormulario": miFormulario})
    