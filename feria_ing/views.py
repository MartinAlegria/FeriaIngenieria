from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import Q
from .models import Project, Categoria
from django.contrib.auth.decorators import login_required
from users.models import Alumno, Profesor
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)


# Create your views here.

@login_required
def home(request):
    context = {
        'projects': Project.objects.all(),
    }
    return render(request, 'feria_ing/home.html', context)

class ProjectDetailView(DetailView):
    model = Project

    def get_context_data(self, **kwargs):
        context = super(ProjectDetailView, self).get_context_data(**kwargs)
        alum = []
        list_al = Alumno.objects.all()
        project_id = self.kwargs['pk']
        ld_user = self.request.user
        mat = ld_user.username.split('@')[0]
        current_user = None
        for al in list_al:
            if al.matricula == mat:
                current_user = al
            if al.proyecto_id == project_id:
                alum.append(al)
        context['alumnos'] = alum
        context['user_current'] = current_user
        return context


def search_bar(request):
    query = request.GET.get('q')
    print(query)
    if query:
        results =  Project.objects.filter(
            Q(nombre__icontains=query)
        )
    
        context = {
            'projects': results
        }
        return render(request, 'feria_ing/home.html', context)
    else:
        return render(request, 'feria_ing/home.html')
    

