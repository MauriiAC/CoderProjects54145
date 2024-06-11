from django import forms
from .models import Curso, Avatar
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import User

# class CursoFormulario(forms.Form):

#   nombre = forms.CharField()
#   camada = forms.IntegerField()

class CursoFormulario(forms.ModelForm):

  class Meta:
    model=Curso
    fields=('__all__')


class ProfesorFormulario(forms.Form):

  nombre = forms.CharField()
  apellido = forms.CharField()
  email = forms.EmailField()
  profesion = forms.CharField()

class UserEditForm(UserChangeForm):

  password = forms.CharField(
    help_text="",
    widget=forms.HiddenInput(), required=False
  )

  password1 = forms.CharField(label="Contraseña", widget=forms.PasswordInput)
  password2 = forms.CharField(label="Repetir contraseña", widget=forms.PasswordInput)

  class Meta:
    model=User
    fields=["email", "first_name", "last_name"]

  def clean_password2(self):

    print(self.cleaned_data)

    password1 = self.cleaned_data["password1"]
    password2 = self.cleaned_data["password2"]

    if password1 != password2:
      raise forms.ValidationError("Las contraseñas deben ser iguales")
    return password2

class AvatarFormulario(forms.ModelForm):

  class Meta:
    model=Avatar
    fields=('imagen',)