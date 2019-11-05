from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages

# Create your views here.

def register(request):
    form = UserCreationForm()

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            print("VALID")
            form.save()
            email = form.cleaned_data.get('email')
            messages.success(request, f'La cuenta fue creada correctamente para {email}')
            return redirect('feria_ing-home')
        else:
            messages.error(request, f'')
    else:
        form = UserCreationForm()
    return render(request, 'users/register.html', {'form':form})
