from django.shortcuts import render
from django.http import HttpResponse
from .models import Project
from django.contrib.auth.decorators import login_required
from users.models import Alumno, Profesor

# Create your views here.

@login_required
def home(request):
    context = {
        'projects': Project.objects.all(),
    }
    return render(request, 'feria_ing/home.html', context)