from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Alumno, Profesor
from . import forms

# Create your views here.

def register(request):

    if request.method == 'POST':
        form = forms.SignUpForm(request.POST)

        if form.is_valid():
            print("VALID")
            email = form.cleaned_data.get('username')
            
            #CHECAR SI ES CORREO DEL TEC
            if ("@itesm.mx" in email) or ("@tec.mx" in email):

                matricula = email.split('@')[0]
                matricula = matricula.upper()
                ##CAMBIAR A QUE SEA A01
                if 'A0' in matricula: #ES ALUMNO
                    nombres = form.cleaned_data.get('nombres')
                    apellidos = form.cleaned_data.get('apellidos')
                    carrera = form.cleaned_data.get('carrera')
                    carrera = carrera.upper()

                    alumno = Alumno(matricula = matricula, 
                    nombres = nombres, apellidos = apellidos, proyecto = None, carrera = carrera)

                    print(alumno)
                    alumno.save()
                    form.save()
                    print("ALUMNO GUARDADO")
                    messages.success(request, f'La cuenta fue creada correctamente para {nombres} {apellidos}. Ya puedes iniciar sesion!')
                    return redirect('login')

                else: #ES PROFE
                    matricula = matricula.lower()
                    nombres = form.cleaned_data.get('nombres')
                    apellidos = form.cleaned_data.get('apellidos')

                    profe = Profesor(matricula = matricula, 
                    nombres = nombres, apellidos = apellidos, profe = True)

                    profe.save()
                    form.save()
                    print("PROFESOR GUARDADO")
                    messages.success(request, f'La cuenta fue creada correctamente para Prof {nombres} {apellidos}')
                    return redirect('feria_ing-home')

            else:
                print("MAIL NO ES DEL TEC")
        
        else:  #ElSE DEL FORM IS VALID
            messages.error(request, f'NO ES VALIDO')
    else:
        form = forms.SignUpForm()
    return render(request, 'users/register.html', {'form':form})


@login_required
def profile(request):
    user = request.user
    mat = user.username.split('@')[0]
    query = Alumno.objects.filter(matricula = mat.upper())
    query2 = Profesor.objects.filter(matricula = mat)
    if query:
        nom = query.first().nombres
        ape = query.first().apellidos
        carr = query.first().carrera

        context = {
            'nombres': nom,
            'apellidos': ape,
            'carrera': carr
         }

    else:
        nom = query2.first().nombres
        ape = query2.first().apellidos

        context = {
            'nombres': nom,
            'apellidos': ape,
            'carrera': user.username
         }

    return render(request, 'users/profile.html', context)
