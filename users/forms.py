# users/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User

class SignUpForm(UserCreationForm):
    nombres = forms.CharField(max_length=140,required=True)
    apellidos = forms.CharField(max_length=140,required=True)
    carrera = forms.CharField(max_length=5, required=False)
    username = forms.CharField(max_length=100, label= 'Email (usa tu correo institucional)')

    class Meta:
        model = User
        fields = ('username','nombres','apellidos','carrera','password1','password2')

