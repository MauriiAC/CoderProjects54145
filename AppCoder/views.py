from django.http import HttpResponse
from django.shortcuts import render
from .models import Curso, Profesor
from .forms import CursoFormulario, ProfesorFormulario
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import DeleteView, UpdateView, CreateView
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.admin.views.decorators import staff_member_required

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

  return render(req, "inicio.html", {})

def cursos(req):

  return render(req, "cursos.html", {})

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

      nuevo_curso = Curso(nombre=data['curso'], camada=data['camada'])
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

  mis_profesores = Profesor.objects.all()

  return render(req, "leer_profesores.html", {"profesores": mis_profesores})

def crea_profesor(req):

  if req.method == 'POST':

    miFormulario = ProfesorFormulario(req.POST)

    if miFormulario.is_valid():

      data = miFormulario.cleaned_data

      nuevo_profesor = Profesor(nombre=data['nombre'], apellido=data['apellido'], email=data['email'], profesion=data['profesion'])
      nuevo_profesor.save()

      return render(req, "inicio.html", {"message": "Profesor creado con éxito"})
    
    else:

      return render(req, "inicio.html", {"message": "Datos inválidos"})
  
  else:

    miFormulario = ProfesorFormulario()

    return render(req, "profesor_formulario.html", {"miFormulario": miFormulario})
  
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