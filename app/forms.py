from dataclasses import field 
from operator  import imod
from django import forms
from django.forms import ModelForm
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class ProductoForm(ModelForm):

    class Meta:
        model= Producto
        fields= '__all__'

        widgets = {
            'fecha_ingreso' : forms.SelectDateWidget(years=range(2020,2023))
        }


class UsuarioForm(ModelForm):

    class Meta:
        model = Usuario
        fields= '__all__'

        widgets = {
            'contraseña_usuario' : forms.PasswordInput
        }

class RegistroUsuarioForm(UserCreationForm):

        class Meta:
            model = User
            fields = ['username','first_name','last_name','email','password1','password2']