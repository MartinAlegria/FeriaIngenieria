from django.shortcuts import render
from django.http import HttpResponse
from . models import Project

# Create your views here.

def home(request):
    context = {
        'projects': Project.objects.all()
    }
    return render(request, 'feria_ing/home.html', context)

def login(request):
    return HttpResponse('<h1> LOGIN <h1>')