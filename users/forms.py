# users/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User

class SignUpForm(UserCreationForm):
    nombres = forms.CharField(max_length=140,required=True)
    apellidos = forms.CharField(max_length=140,required=True)
    carrera = forms.CharField(max_length=5, required=False, label='Carrera (si eres prof, deja esto en blanco)')
    username = forms.CharField(max_length=100, label= 'Email (usa tu correo institucional)')

    class Meta:
        model = User
        fields = ('username','nombres','apellidos','carrera','password1','password2')

class UserLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)

    username = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': '', 'id': 'hello'})
        ,label='Email (Correo institucional)')
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'placeholder': '',
            'id': 'hi',
        }
    ))      