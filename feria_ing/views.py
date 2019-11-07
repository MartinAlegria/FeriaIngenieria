from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import Q
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

def search_bar(request):
    query = request.GET.get('q')
    print(query)
    results = Project.objects.filter(
        Q(nombre__icontains=query)
    )
    
    context = {
        'projects': results
    }
    return render(request, 'feria_ing/home.html', context)
    

