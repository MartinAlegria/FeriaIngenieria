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
                if matricula[0].upper() == 'A': #ES ALUMNO
                    nombres = form.cleaned_data.get('nombres')
                    apellidos = form.cleaned_data.get('apellidos')
                    carrera = form.cleaned_data.get('carrera')
                    carrera = carrera.upper()

                    alumno = Alumno(matricula = matricula, 
                    nombres = nombres, apellidos = apellidos, proyecto = None, carrera = carrera)

                    alumno.save()
                    form.save()
                    print("ALUMNO GUARDADO")
                    messages.success(request, f'La cuenta fue creada correctamente para {nombres} {apellidos}. Ya puedes iniciar sesion!')
                    return redirect('login')

                else: #ES PROFE
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
    query = Alumno.objects.filter(matricula = mat)
    nom = query.first().nombres
    ape = query.first().apellidos
    carr = query.first().carrera

    context = {
        'nombres': nom,
        'apellidos': ape,
        'carrera': carr
    }
    return render(request, 'users/profile.html', context)
